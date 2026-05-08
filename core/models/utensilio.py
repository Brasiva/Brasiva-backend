from django.db import models


class Utensilio(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(blank=False, null=False)
    material = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Utensílio'
        verbose_name_plural = 'Utensílios'
    
    def __str__(self):
        return self.nome
