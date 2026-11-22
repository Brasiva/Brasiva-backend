from rest_framework.serializers import ModelSerializer, SlugRelatedField

from core.models import Funcionario
from uploader.models import Image
from uploader.serializers import ImageSerializer
from rest_framework import serializers


class FuncionarioSerializer(ModelSerializer):
    foto_attachment_key = SlugRelatedField(
        source='foto',
        queryset=Image.objects.all(),
        slug_field='attachment_key',
        required=False,
        write_only=True,
    )
    foto = ImageSerializer(required=False, read_only=True)

    class Meta:
        model = Funcionario
        fields = '__all__'

class FuncionarioListSerializer(ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ('id', 'nome', 'cargo')

    def validate_nome(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'nome' é obrigatório.")
        return value

    def validate_cargo(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'cargo' é obrigatório.")
        return value

    def validate_telefone(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'telefone' é obrigatório.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'email' é obrigatório.")
        return value

    def validate_endereco(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'endereco' é obrigatório.")
        return value


class FuncionarioRetrieveSerializer(ModelSerializer):
    foto = ImageSerializer(required=False)

    class Meta:
        model = Funcionario
        fields = '__all__'
        depth = 1
