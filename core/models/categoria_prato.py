from django.db import models


class CategoriaPrato(models.Model):
    # Agora o nome não se repete e tem uma etiqueta bonita no formulário
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")

    class Meta:
        verbose_name = 'Categoria do Prato'
        verbose_name_plural = 'Categorias dos Pratos'

    def __str__(self):
        return self.nome
