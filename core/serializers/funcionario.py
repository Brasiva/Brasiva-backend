from rest_framework.serializers import ModelSerializer, SlugRelatedField

from core.models import Funcionario
from uploader.models import Image
from uploader.serializers import ImageSerializer


class FuncionarioRetrieveSerializer(ModelSerializer):
    foto = ImageSerializer(required=False)

    class Meta:
        model = Funcionario
        fields = '__all__'
        depth = 1


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
