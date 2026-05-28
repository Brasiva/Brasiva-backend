from django.db import models


class EquipeEvento(models.Model):
    funcionario = models.ForeignKey(
        'Funcionario',
        related_name='equipes_evento',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
    )
    evento = models.ForeignKey(
        'Evento',
        related_name='equipes_evento',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
    )

    class Meta:
        verbose_name = 'Equipe de Evento'
        verbose_name_plural = 'Equipes de Evento'

    def __str__(self):
        return self.funcionario.nome
