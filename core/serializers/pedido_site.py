from decimal import Decimal
from rest_framework import serializers
from core.models import PedidoSite, Prato


class PedidoSiteSerializer(serializers.ModelSerializer):
    itens = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = PedidoSite
        fields = '__all__'
        read_only_fields = ('status', 'total_estimado', 'criado_em')

    def validate_itens(self, itens):
        if not itens:
            raise serializers.ValidationError('Adicione ao menos um produto.')
        seen = set()
        normalized = []
        total = Decimal('0.00')
        for item in itens:
            try:
                prato_id = int(item['prato'])
                quantidade = int(item['quantidade'])
            except (KeyError, TypeError, ValueError):
                raise serializers.ValidationError('Cada item precisa de prato e quantidade válidos.')
            if prato_id in seen or quantidade < 1:
                raise serializers.ValidationError('Itens duplicados ou quantidade inválida.')
            seen.add(prato_id)
            try:
                prato = Prato.objects.get(pk=prato_id, disponivel=True)
            except Prato.DoesNotExist:
                raise serializers.ValidationError('Um dos produtos não está disponível.')
            if prato.valor is None and not prato.sob_orcamento:
                raise serializers.ValidationError('Um produto sem preço precisa estar marcado como sob orçamento.')
            subtotal = prato.valor * quantidade if prato.valor is not None else None
            if subtotal is not None:
                total += subtotal
            normalized.append({
                'prato': prato.pk, 'nome': prato.nome, 'quantidade': quantidade,
                'unidade': prato.unidade, 'sob_orcamento': prato.sob_orcamento,
                'valor_unitario': str(prato.valor) if prato.valor is not None else None,
                'subtotal': str(subtotal) if subtotal is not None else None,
            })
        self._total = total
        return normalized

    def create(self, validated_data):
        validated_data['total_estimado'] = self._total
        return super().create(validated_data)


class PedidoSiteAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoSite
        fields = '__all__'
        read_only_fields = tuple(field.name for field in PedidoSite._meta.fields if field.name != 'status')
