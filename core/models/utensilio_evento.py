from django.db import models


class UtensilioEvento(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='utensilios_vinculados')
    utensilio = models.ForeignKey('Utensilio', on_delete=models.CASCADE, related_name='eventos_vinculados')
    # quantidade = models.IntegerField(default=1) # Se seu diagrama tiver quantidade de utensílios, descomente aqui!

    class Meta:
        verbose_name = 'Utensilio do Evento'
        verbose_name_plural = 'Utensilios do Evento'
        unique_together = ('evento', 'utensilio')

    def __str__(self):
        return f"{self.utensilio.nome} no Evento {self.evento_id}"
