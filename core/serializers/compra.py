from rest_framework.serializers import ModelSerializer

from core.models import Compra


class CompraSerializer(ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

class CompraListSerializer(ModelSerializer):
    class Meta:
        model = Compra
        fields = ('id', 'evento', 'data_compra', 'valor', 'status')

class CompraRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'
        depth = 1