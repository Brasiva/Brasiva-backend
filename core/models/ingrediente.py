from django.db import models


class Ingrediente(models.Model):
    nome = models.CharField(max_length=45)
    und_med = models.CharField(max_length=45, blank=True, null=True)
    categoria_ingrediente = models.ForeignKey(
        'CategoriaIngrediente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingredientes',
    )
    estoque = models.OneToOneField(
        'Estoque',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingrediente',
    )

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'

    def __str__(self):
        return self.nome
