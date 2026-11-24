from django.db import models


class Prato(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, default='')
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unidade = models.CharField(max_length=30, blank=True, default='unidade')
    disponivel = models.BooleanField(default=True)
    sob_orcamento = models.BooleanField(default=False)
    imagem = models.ForeignKey('uploader.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='pratos')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(
        'CategoriaPrato',
        on_delete=models.PROTECT,
        related_name='pratos',
    )
    ingredientes = models.ManyToManyField(
        'Ingrediente',
        through='IngredientePrato'
    )
    modo_fazer = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Prato'
        verbose_name_plural = 'Pratos'

    def __str__(self):
        return self.nome
