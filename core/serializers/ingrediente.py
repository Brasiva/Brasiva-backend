from rest_framework.serializers import ModelSerializer

from core.models import Ingrediente


class IngredienteSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class IngredienteListSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ('id', 'nome', 'valor', 'und_med', 'categoria_ingrediente')

class IngredienteRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'
        depth = 1
