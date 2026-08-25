from rest_framework.serializers import ModelSerializer

from core.models import OrcamentoEvento


class OrcamentoEventoSerializer(ModelSerializer):
    class Meta:
        model = OrcamentoEvento
        fields = '__all__'

class OrcamentoEventoListSerializer(ModelSerializer):
    class Meta:
        model = OrcamentoEvento
        fields = ('id', 'evento', 'valor_total', 'status')

class OrcamentoEventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = OrcamentoEvento
        fields = '__all__'
        depth = 1