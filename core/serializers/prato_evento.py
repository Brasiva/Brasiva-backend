from rest_framework.serializers import ModelSerializer

from core.models import Cardapio


class CardapioSerializer(ModelSerializer):
    class Meta:
        model = Cardapio
        fields = '__all__'
