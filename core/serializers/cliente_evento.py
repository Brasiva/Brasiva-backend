from rest_framework.serializers import ModelSerializer

from core.models import ClienteEvento


class ClienteEventoSerializer(ModelSerializer):
    class Meta:
        model = ClienteEvento
        fields = '__all__'

class ClienteEventoListSerializer(ModelSerializer):
    class Meta:
        model = ClienteEvento
        fields = ('id', 'cliente', 'evento')

class ClienteEventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = ClienteEvento
        fields = '__all__'
        depth = 1