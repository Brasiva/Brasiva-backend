from rest_framework.serializers import ModelSerializer

from core.models import Evento


class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class EventoListSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = ('id', 'data_hora', 'local', 'tipo_evento', 'endereco', 'status')

class EventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        depth = 1
