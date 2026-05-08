from rest_framework.serializers import ModelSerializer

from core.models import Endereco, Evento


class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'


class EnderecoSerializer(ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'
