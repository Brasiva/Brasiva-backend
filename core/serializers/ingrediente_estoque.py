from rest_framework.serializers import ModelSerializer

from core.models import IngredienteEstoque


class IngredienteEstoqueSerializer(ModelSerializer):
    class Meta:
        model = IngredienteEstoque
        fields = '__all__'
