from rest_framework.serializers import ModelSerializer
from core.models import Notificacao


class NotificacaoSerializer(ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ('id', 'titulo', 'mensagem', 'tipo', 'lida', 'data')
        read_only_fields = ('id', 'titulo', 'mensagem', 'tipo', 'data')
