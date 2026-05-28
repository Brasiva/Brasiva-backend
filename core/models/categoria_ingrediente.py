from django.db import models


class CategoriaIngrediente(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria do Ingrediente'
        verbose_name_plural = 'Categorias dos Ingredientes'

    def __str__(self):
        return self.nome
