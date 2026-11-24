from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from core.models import Notificacao, PedidoSite, User
from core.serializers import PedidoSiteAdminSerializer, PedidoSiteSerializer


class PedidoSiteViewSet(ModelViewSet):
    queryset = PedidoSite.objects.all()
    serializer_class = PedidoSiteSerializer

    def get_serializer_class(self):
        return PedidoSiteSerializer if self.action == 'create' else PedidoSiteAdminSerializer

    def get_permissions(self):
        return [AllowAny()] if self.action == 'create' else [IsAdminUser()]

    def perform_create(self, serializer):
        pedido = serializer.save()
        usuarios = User.objects.filter(is_staff=True, is_active=True)
        Notificacao.objects.bulk_create([
            Notificacao(usuario=usuario, titulo='Nova solicitação de evento',
                        mensagem=f'{pedido.nome} enviou uma solicitação para {pedido.tipo_evento}.', tipo='info')
            for usuario in usuarios
        ])
