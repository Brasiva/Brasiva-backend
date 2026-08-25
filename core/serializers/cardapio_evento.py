from rest_framework.serializers import ModelSerializer

from core.models import CardapioEvento


class CardapioEventoSerializer(ModelSerializer):
    class Meta:
        model = CardapioEvento
        fields = '__all__'

class CardapioEventoListSerializer(ModelSerializer):
    class Meta:
        model = CardapioEvento
        fields = ('id', 'evento', 'prato')

class CardapioEventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = CardapioEvento
        fields = '__all__'
        depth = 1
