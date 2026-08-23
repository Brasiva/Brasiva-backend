from django.db import models


class Estoque(models.Model):
    quantidade = models.PositiveIntegerField(default=0)
    und_medida = models.CharField(max_length=20, verbose_name='Unidade de Medida')

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return f"{self.quantidade} {self.und_medida}"
