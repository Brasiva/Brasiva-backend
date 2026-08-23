from django.db import models


class CardapioEvento(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='prato_cardapio')
    prato = models.ForeignKey('Prato', on_delete=models.CASCADE, related_name='evento_cardapio')

    class Meta:
        verbose_name = 'Cardápio'
        verbose_name_plural = 'Cardápios'

    def __str__(self):
        return f'Cardápio {self.prato.nome} - {self.evento}'
