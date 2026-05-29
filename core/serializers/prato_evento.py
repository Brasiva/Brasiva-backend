from rest_framework.serializers import ModelSerializer

from core.models import PratoEvento


class PratoEventoSerializer(ModelSerializer):
    class Meta:
        model = PratoEvento
        fields = '__all__'
