from django.db import models


class Compra(models.Model):
    STATUS_PENDENTE = 'pendente'
    STATUS_CONCLUIDA = 'concluida'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_CONCLUIDA, 'Concluída'),
    ]
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='compras')
    data_compra = models.DateTimeField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        if self.data_compra:
            return f'Compra de {self.data_compra.strftime("%d/%m/%Y")}'
        return f'Compra #{self.id} (pendente)'
