from rest_framework.serializers import ModelSerializer

from core.models import ItemCompra


class ItemCompraSerializer(ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = '__all__'

class ItemCompraListSerializer(ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ('id', 'compra', 'ingrediente', 'nome', 'quantidade')

class ItemCompraRetrieveSerializer(ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = '__all__'
        depth = 1