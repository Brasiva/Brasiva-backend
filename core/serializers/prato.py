from rest_framework.serializers import ModelSerializer

from core.models import Prato


class PratoSerializer(ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'
