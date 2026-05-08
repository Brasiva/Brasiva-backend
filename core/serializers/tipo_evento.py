from rest_framework.serializers import ModelSerializer

from core.models import TipoEvento


class TipoEventoSerializer(ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = '__all__'
