from rest_framework.serializers import ModelSerializer

from core.models import Prato


class PratoSerializer(ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'

class PratoListSerializer(ModelSerializer):
    class Meta:
        model = Prato
        fields = ('id', 'nome', 'categoria', 'valor', 'modo_fazer', 'descricao', 'unidade', 'disponivel', 'sob_orcamento')

class PratoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'
        depth = 1
