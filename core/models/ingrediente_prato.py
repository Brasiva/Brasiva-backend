from django.db import models


class IngredientePrato(models.Model):
    ingrediente = models.ForeignKey('Ingrediente', on_delete=models.CASCADE)
    prato = models.ForeignKey('Prato', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    class Meta:
        unique_together = ('prato', 'ingrediente')
        verbose_name = 'Ingrediente do Prato'
        verbose_name_plural = 'Ingredientes dos Pratos'

    def __str__(self):
        return f"{self.quantidade} de {self.ingrediente.nome} no {self.prato.nome}"