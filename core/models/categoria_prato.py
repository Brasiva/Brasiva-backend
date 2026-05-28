from django.db import models


class CategoriaPrato(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria do Prato'
        verbose_name_plural = 'Categorias dos Pratos'

    def __str__(self):
        return self.nome
