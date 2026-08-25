from rest_framework.serializers import ModelSerializer

from core.models import Ingrediente


class IngredienteSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class IngredienteListSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ('id', 'nome', 'categoria_ingrediente')

class IngredienteRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'
        depth = 1