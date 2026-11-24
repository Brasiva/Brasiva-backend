from datetime import datetime, time
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone
from django.utils.html import format_html, format_html_join
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

    @action(detail=True, methods=['post'], url_path='salvar-orcamento')
    def salvar_orcamento(self, request, pk=None):
        pedido = self.get_object()
        if not pedido.evento_id:
            return Response({'detail': 'Aceite o pedido antes de preparar o orçamento.'}, status=status.HTTP_409_CONFLICT)
        try:
            valor = Decimal(str(request.data.get('valor_final')))
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError({'valor_final': 'Informe um valor final válido.'})
        if not valor.is_finite() or valor < 0:
            raise ValidationError({'valor_final': 'O valor final não pode ser negativo.'})

        with transaction.atomic():
            pedido = PedidoSite.objects.select_for_update().get(pk=pedido.pk)
            if pedido.orcamento_enviado_em:
                return Response({'detail': 'Este orçamento já foi enviado e não pode ser alterado.'}, status=status.HTTP_409_CONFLICT)
            orcamento = OrcamentoEvento.objects.select_for_update().get(evento_id=pedido.evento_id)
            orcamento.valor_total = valor
            orcamento.save(update_fields=['valor_total'])
            pedido.orcamento_final = valor
            pedido.save(update_fields=['orcamento_final'])
        return Response({'id': pedido.id, 'valor_final': str(valor), 'salvo': True})

    @action(detail=True, methods=['post'], url_path='enviar-orcamento')
    def enviar_orcamento(self, request, pk=None):
        if not settings.EMAIL_HOST:
            return Response({'detail': 'Envio indisponível: configure o servidor SMTP do Brasiva.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        enviado_em = timezone.now()
        with transaction.atomic():
            pedido = PedidoSite.objects.select_for_update().get(pk=self.get_object().pk)
            if not pedido.evento_id:
                return Response({'detail': 'Aceite o pedido antes de enviar o orçamento.'}, status=status.HTTP_409_CONFLICT)
            if pedido.orcamento_final is None:
                return Response({'detail': 'Defina e salve o valor final antes de enviar.'}, status=status.HTTP_409_CONFLICT)
            if pedido.orcamento_enviado_em:
                return Response({'detail': 'Este orçamento já foi enviado ao cliente.'}, status=status.HTTP_409_CONFLICT)
            pedido.orcamento_enviado_em = enviado_em
            pedido.save(update_fields=['orcamento_enviado_em'])

        evento = pedido.evento
        endereco = evento.endereco
        endereco_evento = ', '.join(filter(None, (
            endereco.logradouro, str(endereco.numero or ''), endereco.complemento,
            endereco.bairro, endereco.cidade, endereco.estado, endereco.cep,
        )))
        itens = pedido.itens or []
        itens_texto = '\n'.join(f"• {item.get('quantidade', 0)} × {item.get('nome', 'Produto')}" for item in itens)
        itens_html = format_html_join('', '<li>{} × {}</li>', (
            (item.get('quantidade', 0), item.get('nome', 'Produto')) for item in itens
        ))
        data_evento = timezone.localtime(evento.data_hora).strftime('%d/%m/%Y às %H:%M')
        valor = pedido.orcamento_final
        consulta = (
            f"{settings.BRASIVA_SITE_URL.rstrip('/')}/pedido/confirmado/{pedido.token_consulta}"
            if settings.BRASIVA_SITE_URL else f"Código de consulta: {pedido.token_consulta}"
        )
        consulta_html = (
            format_html('<p><a href="{}">Consultar pedido e orçamento</a></p>', consulta)
            if settings.BRASIVA_SITE_URL
            else format_html('<p><strong>Código de consulta:</strong> {}</p>', pedido.token_consulta)
        )
        mensagem = (
            f"Olá, {pedido.nome}!\n\n"
            f"Preparamos com cuidado o orçamento do seu evento. Seguem os detalhes da solicitação:\n\n"
            f"Pedido: #{pedido.id}\nEvento: {evento.tipo_evento.nome}\nData e horário: {data_evento}\n"
            f"Convidados: {evento.quantidade_pessoas}\nEndereço: {endereco_evento}\n\n"
            f"Produtos e quantidades:\n{itens_texto}\n\n"
            f"Valor final: R$ {valor:.2f}\n\nConsulte o orçamento: {consulta}\n\n"
            f"Atenciosamente,\nEquipe Brasiva\nContato: {settings.DEFAULT_FROM_EMAIL}"
        )
        try:
            email = EmailMultiAlternatives(
                f'Orçamento Brasiva para o pedido #{pedido.id}', mensagem,
                settings.DEFAULT_FROM_EMAIL, [pedido.email],
            )
            email.attach_alternative(format_html(
                '<div style="font-family:Arial,sans-serif;color:#352820;max-width:640px;margin:auto">'
                '<h1 style="color:#813c2c">Orçamento Brasiva</h1><p>Olá, <strong>{}</strong>!</p>'
                '<p>Preparamos com cuidado o orçamento do seu evento. Confira os dados:</p>'
                '<p><strong>Pedido:</strong> #{}<br><strong>Evento:</strong> {}<br>'
                '<strong>Data e horário:</strong> {}<br><strong>Convidados:</strong> {}<br>'
                '<strong>Endereço:</strong> {}</p><h2>Produtos e quantidades</h2><ul>{}</ul>'
                '<p style="font-size:20px"><strong>Valor final: R$ {}</strong></p>{}'
                '<p>Atenciosamente,<br>Equipe Brasiva<br>Contato: {}</p></div>',
                pedido.nome, pedido.id, evento.tipo_evento.nome, data_evento,
                evento.quantidade_pessoas, endereco_evento, itens_html, f'{valor:.2f}',
                consulta_html, settings.DEFAULT_FROM_EMAIL,
            ), 'text/html')
            if not email.send(fail_silently=False):
                raise RuntimeError('O servidor SMTP não confirmou o envio.')
        except Exception:
            PedidoSite.objects.filter(pk=pedido.pk, orcamento_enviado_em=enviado_em).update(orcamento_enviado_em=None)
            return Response({
                'detail': 'Não foi possível enviar o e-mail. O orçamento continua salvo e pode ser enviado novamente.',
            }, status=status.HTTP_502_BAD_GATEWAY)
        return Response({'id': pedido.id, 'valor_final': str(valor), 'email_enviado': True})
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
