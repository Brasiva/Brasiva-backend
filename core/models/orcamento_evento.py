from django.db import models
from decimal import Decimal


class OrcamentoEvento(models.Model):
    evento = models.OneToOneField('Evento', on_delete=models.CASCADE, related_name='orcamento')
    mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Orçamento do Evento'
        verbose_name_plural = 'Orçamentos dos Eventos'

    @property
    def valor_total_pratos(self):
        """Calcula: (Valor do Prato x Quantidade) para todos os pratos do evento"""
        total = Decimal('0.00')
        # Buscamos a tabela intermediária que criamos antes
        pratos_vinculados = self.evento.pratos_vinculados.all()
        for pv in pratos_vinculados:
            total += pv.prato.valor * pv.quantidade
        return total

    @property
    def valor_total_equipe(self):
        """Soma o custo de todos os funcionários escalados para o evento"""
        total = Decimal('0.00')
        equipes = self.evento.equipes_vinculadas.all()
        for ev in equipes:
            total += ev.funcionario.pagamento
        return total

    @property
    def valor_total_orcamento(self):
        """Soma tudo: Mão de obra + Taxa do Evento + Pratos + Equipe"""
        taxa_utensilio = self.evento.taxa_utensilio or Decimal('0.00')
        
        return (
            self.mao_de_obra + 
            taxa_utensilio + 
            self.valor_total_pratos + 
            self.valor_total_equipe
        )

    def __str__(self):
        return f"Orçamento do Evento {self.evento_id} - Total: R$ {self.valor_total_orcamento}"
