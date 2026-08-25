from rest_framework.serializers import ModelSerializer

from core.models import UtensilioEvento


class UtensilioEventoSerializer(ModelSerializer):
    class Meta:
        model = UtensilioEvento
        fields = '__all__'

class UtensilioEventoListSerializer(ModelSerializer):
    class Meta:
        model = UtensilioEvento
        fields = ('id', 'evento', 'utensilio', 'quantidade')

class UtensilioEventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = UtensilioEvento
        fields = '__all__'
        depth = 1