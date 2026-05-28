from rest_framework.serializers import ModelSerializer

from core.models import ItemCompra


class ItemCompraSerializer(ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = '__all__'
