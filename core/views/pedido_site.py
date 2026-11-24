from datetime import datetime, time
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.models import (
    CardapioEvento, Cliente, ClienteEvento, Endereco, Evento, Notificacao,
    OrcamentoEvento, PedidoSite, Prato, TipoEvento, User,
)
from core.serializers import PedidoSiteAdminSerializer, PedidoSiteSerializer


class PedidoSiteViewSet(ModelViewSet):
    queryset = PedidoSite.objects.all()
    serializer_class = PedidoSiteSerializer

    def get_serializer_class(self):
        return PedidoSiteSerializer if self.action == 'create' else PedidoSiteAdminSerializer

    def get_permissions(self):
        return [AllowAny()] if self.action in ('create', 'consultar_orcamento') else [IsAdminUser()]

    def perform_create(self, serializer):
        pedido = serializer.save()
        usuarios = User.objects.filter(is_staff=True, is_active=True)
        Notificacao.objects.bulk_create([
            Notificacao(usuario=usuario, titulo='Nova solicitação de evento',
                        mensagem=f'{pedido.nome} enviou uma solicitação para {pedido.tipo_evento}.', tipo='info')
            for usuario in usuarios
        ])

    def perform_update(self, serializer):
        with transaction.atomic():
            pedido = serializer.save()
            if pedido.status == 'aprovado':
                self._encaminhar_para_eventos(pedido)

    def _encaminhar_para_eventos(self, pedido):
        if pedido.evento_id:
            return pedido.evento

        address = pedido.endereco_evento or {}
        try:
            number = int(address.get('numero')) if str(address.get('numero', '')).strip() else None
        except (TypeError, ValueError):
            number = None
        endereco = Endereco.objects.create(
            logradouro=address['logradouro'], numero=number, bairro=address['bairro'],
            cidade=address['cidade'], estado=address['estado'].upper()[:2],
            cep=address.get('cep') or None, complemento=address.get('complemento') or None,
        )
        cliente, _ = Cliente.objects.update_or_create(
            email=pedido.email,
            defaults={'nome': pedido.nome, 'telefone': pedido.telefone[:15]},
        )
        tipo, _ = TipoEvento.objects.get_or_create(
            nome=pedido.tipo_evento,
            defaults={'cor': '#E8DCCB'},
        )
        horario = pedido.horario_evento or time(12, 0)
        data_hora = timezone.make_aware(
            datetime.combine(pedido.data_evento, horario), timezone.get_current_timezone(),
        )
        evento = Evento.objects.create(
            quantidade_pessoas=pedido.convidados, data_hora=data_hora,
            taxa_utensilio=Decimal('0.00'), endereco=endereco, tipo_evento=tipo,
            local=f"{endereco.logradouro}, {endereco.numero or 's/n'} - {endereco.bairro}, {endereco.cidade}/{endereco.estado}",
        )
        ClienteEvento.objects.get_or_create(cliente=cliente, evento=evento)
        menu_items = []
        for item in pedido.itens:
            try:
                dish = Prato.objects.get(pk=item['prato'])
            except (Prato.DoesNotExist, KeyError):
                continue
            menu_items.append(CardapioEvento(evento=evento, prato=dish))
        CardapioEvento.objects.bulk_create(menu_items, ignore_conflicts=True)
        OrcamentoEvento.objects.get_or_create(evento=evento, defaults={'mao_de_obra': Decimal('0.00')})
        pedido.evento = evento
        pedido.save(update_fields=['evento'])
        return evento

    @action(detail=True, methods=['post'], url_path='enviar-orcamento')
    def enviar_orcamento(self, request, pk=None):
        pedido = self.get_object()
        if not pedido.evento_id:
            return Response({'detail': 'Aceite o pedido antes de enviar o orçamento.'}, status=status.HTTP_409_CONFLICT)
        try:
            valor = Decimal(str(request.data.get('valor_final')))
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError({'valor_final': 'Informe um valor final válido.'})
        if not valor.is_finite() or valor < 0:
            raise ValidationError({'valor_final': 'O valor final não pode ser negativo.'})

        with transaction.atomic():
            orcamento = OrcamentoEvento.objects.select_for_update().get(evento_id=pedido.evento_id)
            orcamento.valor_total = valor
            orcamento.save(update_fields=['valor_total'])
            pedido.orcamento_final = valor
            pedido.save(update_fields=['orcamento_final'])

        if not settings.EMAIL_HOST:
            return Response({
                'id': pedido.id, 'valor_final': str(valor), 'email_enviado': False,
                'detail': 'Orçamento salvo. Configure EMAIL_HOST no backend para habilitar o envio por e-mail.',
            }, status=status.HTTP_200_OK)

        link = f"{settings.BRASIVA_SITE_URL.rstrip('/')}/pedido/confirmado/{pedido.token_consulta}" if settings.BRASIVA_SITE_URL else str(pedido.token_consulta)
        mensagem = (
            f"Olá, {pedido.nome}!\n\nO orçamento do seu pedido #{pedido.id} foi finalizado.\n"
            f"Valor final: R$ {valor:.2f}\n\nConsulte os detalhes usando este link ou código:\n{link}\n"
        )
        try:
            enviados = send_mail(
                f'Orçamento Brasiva para o pedido #{pedido.id}', mensagem,
                settings.DEFAULT_FROM_EMAIL, [pedido.email], fail_silently=False,
            )
        except Exception as error:
            return Response({
                'id': pedido.id, 'valor_final': str(valor), 'email_enviado': False,
                'detail': f'Orçamento salvo, mas o e-mail não foi enviado: {error}',
            }, status=status.HTTP_502_BAD_GATEWAY)
        if enviados:
            pedido.orcamento_enviado_em = timezone.now()
            pedido.save(update_fields=['orcamento_enviado_em'])
        return Response({'id': pedido.id, 'valor_final': str(valor), 'email_enviado': bool(enviados)})

    @action(detail=False, methods=['get'], url_path='consulta-orcamento')
    def consultar_orcamento(self, request):
        token = request.query_params.get('token')
        if not token:
            raise ValidationError({'token': 'Informe o código de consulta do pedido.'})
        try:
            pedido = PedidoSite.objects.get(token_consulta=token)
        except (PedidoSite.DoesNotExist, ValueError):
            return Response({'detail': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'id': pedido.id, 'nome': pedido.nome, 'tipo_evento': pedido.tipo_evento,
            'data_evento': pedido.data_evento, 'horario_evento': pedido.horario_evento,
            'itens': pedido.itens, 'total_estimado': pedido.total_estimado,
            'orcamento_final': pedido.orcamento_final,
            'orcamento_enviado_em': pedido.orcamento_enviado_em,
            'status': pedido.status,
        })
