from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Prato


class PratoSerializer(ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'

class PratoListSerializer(ModelSerializer):
    imagem_url = serializers.SerializerMethodField()

    class Meta:
        model = Prato
        fields = ('id', 'nome', 'categoria', 'valor', 'modo_fazer', 'descricao', 'unidade', 'disponivel', 'sob_orcamento', 'imagem_url')

    def get_imagem_url(self, prato):
        if not prato.imagem_id or not prato.imagem.file:
            return None
        url = prato.imagem.file.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request and url.startswith('/') else url

class PratoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'
        depth = 1
