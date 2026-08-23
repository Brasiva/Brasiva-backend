from django.db import models


class OrcamentoEvento(models.Model):
    evento = models.OneToOneField('Evento', on_delete=models.CASCADE, related_name='orcamento')
    mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Orçamento do Evento'
        verbose_name_plural = 'Orçamentos dos Eventos'

    def __str__(self):
        return f"Orçamento do Evento {self.evento_id} - Total: R$ {self.valor_total}"
