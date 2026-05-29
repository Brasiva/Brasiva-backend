from rest_framework.serializers import ModelSerializer

from core.models import UtensilioEvento


class UtensilioEventoSerializer(ModelSerializer):
    class Meta:
        model = UtensilioEvento
        fields = '__all__'
