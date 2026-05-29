from django.db import models


class IngredienteEstoque(models.Model):
    nome = models.CharField(max_length=45)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Ingrediente em Estoque'
        verbose_name_plural = 'Ingredientes em Estoque'

    def __str__(self):
        return self.nome
