from django.db import models


class Estoque(models.Model):
    # Usar unique=True evita cadastrar "Arroz" duas vezes em linhas separadas
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Item")
    # Dica: 'KG', 'Unidade', 'Litros', etc.
    und_medida = models.CharField(max_length=20, verbose_name="Unidade de Medida")

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return f"{self.nome} ({self.quantidade} {self.und_medida})"