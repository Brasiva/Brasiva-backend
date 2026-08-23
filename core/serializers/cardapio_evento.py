from rest_framework.serializers import ModelSerializer

from core.models import CardapioEvento


class CardapioEventoSerializer(ModelSerializer):
    class Meta:
        model = CardapioEvento
        fields = '__all__'
