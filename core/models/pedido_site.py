from django.db import models


class PedidoSite(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('em_analise', 'Em análise'),
        ('contatado', 'Contatado'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
    ]
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=30)
    tipo_evento = models.CharField(max_length=100)
    data_evento = models.DateField()
    convidados = models.PositiveIntegerField()
    observacoes = models.TextField(blank=True, default='')
    itens = models.JSONField(default=list)
    total_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{self.pk} — {self.nome}'
