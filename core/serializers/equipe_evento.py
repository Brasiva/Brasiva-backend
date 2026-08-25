from rest_framework.serializers import ModelSerializer

from core.models import EquipeEvento


class EquipeEventoSerializer(ModelSerializer):
    class Meta:
        model = EquipeEvento
        fields = '__all__'

class EquipeEventoListSerializer(ModelSerializer):
    class Meta:
        model = EquipeEvento
        fields = ('id', 'evento', 'funcionario')

class EquipeEventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = EquipeEvento
        fields = '__all__'
        depth = 1