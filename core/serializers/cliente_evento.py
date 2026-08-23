from rest_framework.serializers import ModelSerializer

from core.models import ClienteEvento


class ClienteEventoSerializer(ModelSerializer):
    class Meta:
        model = ClienteEvento
        fields = '__all__'
