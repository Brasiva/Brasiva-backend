from rest_framework.serializers import ModelSerializer

from core.models import CategoriaIngrediente


class CategoriaIngredienteSerializer(ModelSerializer):
    class Meta:
        model = CategoriaIngrediente
        fields = '__all__'
