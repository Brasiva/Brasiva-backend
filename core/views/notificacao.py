from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.models import Notificacao
from core.serializers import NotificacaoSerializer


class NotificacaoViewSet(ModelViewSet):
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user)

    @action(detail=False, methods=['post'], url_path='marcar-todas-lidas')
    def marcar_todas_lidas(self, request):
        self.get_queryset().filter(lida=False).update(lida=True)
        return Response({'atualizadas': True})

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
