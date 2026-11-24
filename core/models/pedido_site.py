from django.db import models
from uuid import uuid4


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
    horario_evento = models.TimeField(null=True, blank=True)
    endereco_evento = models.JSONField(default=dict, blank=True)
    convidados = models.PositiveIntegerField()
    observacoes = models.TextField(blank=True, default='')
    itens = models.JSONField(default=list)
    total_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    orcamento_final = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    orcamento_enviado_em = models.DateTimeField(null=True, blank=True)
    token_consulta = models.UUIDField(default=uuid4, unique=True, editable=False)
    evento = models.OneToOneField(
        'Evento', null=True, blank=True, on_delete=models.SET_NULL, related_name='pedido_site',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{self.pk} — {self.nome}'
