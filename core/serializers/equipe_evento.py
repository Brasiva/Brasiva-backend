from rest_framework.serializers import ModelSerializer

from core.models import EquipeEvento


class EquipeEventoSerializer(ModelSerializer):
    class Meta:
        model = EquipeEvento
        fields = '__all__'
