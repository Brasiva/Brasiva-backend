from rest_framework.serializers import ModelSerializer

from core.models import Convite


class ConviteSerializer(ModelSerializer):
    class Meta:
        model = Convite
        fields = '__all__'
        extra_kwargs = {
            'token_hash': {'write_only': True},
        }


class ConviteListSerializer(ModelSerializer):
    class Meta:
        model = Convite
        fields = ('id', 'funcionario', 'grupo', 'usado', 'expira_em')


class ConviteRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Convite
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            'token_hash': {'write_only': True},
        }
