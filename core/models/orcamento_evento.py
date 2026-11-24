from decimal import Decimal

from django.db import models


class OrcamentoEvento(models.Model):
    STATUS_PENDENTE = 'pendente'
    STATUS_APROVADO = 'aprovado'
    STATUS_RECUSADO = 'recusado'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_APROVADO, 'Aprovado'),
        (STATUS_RECUSADO, 'Recusado'),
    ]

    evento = models.OneToOneField('Evento', on_delete=models.CASCADE, related_name='orcamento')
    mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    @property
    def valor_total_pratos(self):
        pratos = (item.prato for item in self.evento.prato_cardapio.select_related('prato').all())
        return sum((prato.valor or Decimal('0.00') for prato in pratos), Decimal('0.00'))

    @property
    def valor_total_equipe(self):
        return sum((item.pagamento or Decimal('0.00') for item in self.evento.funcionarios_vinculados.all()), Decimal('0.00'))

    @property
    def valor_total_orcamento(self):
        return self.valor_total_pratos + self.valor_total_equipe + self.mao_de_obra + (self.evento.taxa_utensilio or Decimal('0.00'))

    class Meta:
        verbose_name = 'Orçamento do Evento'
        verbose_name_plural = 'Orçamentos dos Eventos'

    def __str__(self):
        return f"Orçamento do Evento {self.evento_id} - Total: R$ {self.valor_total}"
