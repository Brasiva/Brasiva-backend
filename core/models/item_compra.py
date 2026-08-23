from django.db import models


class ItemCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='itens')
    ingrediente = models.ForeignKey(
        'Ingrediente',
        on_delete=models.PROTECT,
        related_name='compras',
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=100, blank=True, null=True)
    quantidade = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Item de Compra'
        verbose_name_plural = 'Itens de Compra'

    def __str__(self):
        if self.ingrediente:
            return f'{self.quantidade} de {self.ingrediente.nome}'
        return f'{self.quantidade} de {self.nome}'
