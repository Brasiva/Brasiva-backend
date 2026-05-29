from django.db import models


class EquipeEvento(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE, related_name='equipes_vinculadas')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='funcionarios_vinculados')

    class Meta:
        verbose_name = 'Equipe de Evento'
        verbose_name_plural = 'Equipes de Evento'
        unique_together = ('funcionario', 'evento')

    def __str__(self):
        return f"{self.funcionario.nome} no Evento {self.evento_id}"
