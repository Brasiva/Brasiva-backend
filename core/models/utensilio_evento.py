from django.db import models



class UtensilioEvento(models.Model):
    evento = models.ForeignKey(
        'Evento',
        related_name='utensilios_evento',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        default=None,
    )
    utensilio = models.ForeignKey(
        'Utensilio',
        related_name='eventos_utensilio',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        default=None,
    )

    class Meta:
        verbose_name = 'Utensilio do Evento'
        verbose_name_plural = 'Utensilios do Evento'

    def __str__(self):
        return self.nome
