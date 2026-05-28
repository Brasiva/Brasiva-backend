from rest_framework.serializers import ModelSerializer

from core.models import CategoriaPrato


class CategoriaPratoSerializer(ModelSerializer):
    class Meta:
        model = CategoriaPrato
        fields = '__all__'
