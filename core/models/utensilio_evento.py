from django.db import models


class UtensilioEvento(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='utensilios_vinculados')
    utensilio = models.ForeignKey('Utensilio', on_delete=models.CASCADE, related_name='eventos_vinculados')
    quantidade = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Utensílio do Evento'
        verbose_name_plural = 'Utensílios do Evento'
        unique_together = ('evento', 'utensilio')

    def __str__(self):
        return f"{self.utensilio.nome} no Evento {self.evento_id}"
