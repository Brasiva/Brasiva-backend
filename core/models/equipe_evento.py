from django.db import models


class EquipeEvento(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE, related_name='equipes_vinculadas')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='funcionarios_vinculados')
    pagamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Equipe do Evento'
        verbose_name_plural = 'Equipes do Evento'
        unique_together = ('funcionario', 'evento')

    def __str__(self):
        return f"{self.funcionario.nome} no Evento {self.evento_id}"
