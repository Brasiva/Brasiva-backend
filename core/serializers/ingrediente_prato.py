from rest_framework.serializers import ModelSerializer

from core.models import IngredientePrato


class IngredientePratoSerializer(ModelSerializer):
    class Meta:
        model = IngredientePrato
        fields = '__all__'

class IngredientePratoListSerializer(ModelSerializer):
    class Meta:
        model = IngredientePrato
        fields = ('id', 'ingrediente', 'prato', 'quantidade')

class IngredientePratoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = IngredientePrato
        fields = '__all__'
        depth = 1