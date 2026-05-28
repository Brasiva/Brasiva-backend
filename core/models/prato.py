from django.db import models


class Prato(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Prato'
        verbose_name_plural = 'Pratos'

    def __str__(self):
        return self.nome
