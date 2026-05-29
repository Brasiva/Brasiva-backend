from rest_framework import serializers

from core.models import OrcamentoEvento


class OrcamentoEventoSerializer(serializers.ModelSerializer):
    # Expomos os métodos de cálculo (@property) da model como campos de leitura na API
    valor_total_pratos = serializers.ReadOnlyField()
    valor_total_equipe = serializers.ReadOnlyField()
    valor_total_orcamento = serializers.ReadOnlyField()

    class Meta:
        model = OrcamentoEvento
        fields = [
            'id', 
            'evento', 
            'mao_de_obra', 
            'valor_total_pratos', 
            'valor_total_equipe', 
            'valor_total_orcamento'
        ]
