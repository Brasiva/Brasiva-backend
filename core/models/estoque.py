from django.db import models


class Estoque(models.Model):
    quantidade = models.PositiveIntegerField(blank=False, null=False)
    und = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return self.quantidade
