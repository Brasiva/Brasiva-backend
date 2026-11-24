from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import CategoriaPrato


class CategoriaPratoSerializer(ModelSerializer):
    quantidade_opcoes = SerializerMethodField()
    quantidade_disponiveis = SerializerMethodField()

    class Meta:
        model = CategoriaPrato
        fields = ('id', 'nome', 'publicada', 'quantidade_opcoes', 'quantidade_disponiveis')
        read_only_fields = ('quantidade_opcoes', 'quantidade_disponiveis')

    def get_quantidade_opcoes(self, categoria):
        return categoria.pratos.count()

    def get_quantidade_disponiveis(self, categoria):
        from django.db.models import Q
        return categoria.pratos.filter(disponivel=True).filter(Q(valor__isnull=False) | Q(sob_orcamento=True)).count()
