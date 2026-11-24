from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import CategoriaPrato


class CategoriaPratoSerializer(ModelSerializer):
    quantidade_opcoes = SerializerMethodField()

    class Meta:
        model = CategoriaPrato
        fields = ('id', 'nome', 'publicada', 'quantidade_opcoes')
        read_only_fields = ('quantidade_opcoes',)

    def get_quantidade_opcoes(self, categoria):
        from django.db.models import Q
        return categoria.pratos.filter(disponivel=True).filter(Q(valor__isnull=False) | Q(sob_orcamento=True)).count()
