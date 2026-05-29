from django.db import models


class PratoEvento(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='pratos_vinculados')
    prato = models.ForeignKey('Prato', on_delete=models.CASCADE, related_name='eventos_vinculados')
    quantidade = models.IntegerField() # Esse campo veio direto do seu diagrama!

    class Meta:
        verbose_name = 'Prato do Evento'
        verbose_name_plural = 'Pratos do Evento'
        unique_together = ('evento', 'prato')

    def __str__(self):
        return f"{self.quantidade}x {self.prato.nome} no Evento {self.evento_id}"
