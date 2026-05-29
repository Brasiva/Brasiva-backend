from rest_framework.serializers import ModelSerializer

from core.models import IngredientePrato


class IngredientePratoSerializer(ModelSerializer):
    class Meta:
        model = IngredientePrato
        fields = '__all__'
