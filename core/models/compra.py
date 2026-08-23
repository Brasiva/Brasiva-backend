from django.db import models


class Compra(models.Model):
    data_compra = models.DateTimeField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        if self.data_compra:
            return f'Compra de {self.data_compra.strftime("%d/%m/%Y")}'
        return f'Compra #{self.id} (pendente)'
