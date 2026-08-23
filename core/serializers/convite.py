from rest_framework.serializers import ModelSerializer

from core.models import Convite


class ConviteSerializer(ModelSerializer):
    class Meta:
        model = Convite
        fields = '__all__'
        extra_kwargs = {
            'token_hash': {'write_only': True},
        }