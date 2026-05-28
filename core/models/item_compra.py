from django.db import models


class ItemCompra(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(blank=False, null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item de Compra'
        verbose_name_plural = 'Itens de Compra'

    def __str__(self):
        return self.nome
