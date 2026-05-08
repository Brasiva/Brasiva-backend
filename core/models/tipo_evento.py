from colorfield.fields import ColorField
from django.db import models


class TipoEvento(models.Model):
    nome = models.CharField(max_length=100)
    cor = ColorField(default='#FF0000')

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipos de Eventos'

    def __str__(self):
        return self.nome
