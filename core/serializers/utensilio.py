from rest_framework.serializers import ModelSerializer

from core.models import Utensilio


class UtensilioSerializer(ModelSerializer):
    class Meta:
        model = Utensilio
        fields = '__all__'
