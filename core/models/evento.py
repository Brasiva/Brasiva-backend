from django.db import models


from .endereco import Endereco

class Evento(models.Model):
    STATUS_CONFIRMADO = 'confirmado'
    STATUS_EM_ANDAMENTO = 'em_andamento'
    STATUS_CONCLUIDO = 'concluido'
    STATUS_CANCELADO = 'cancelado'

    STATUS_CHOICES = [
        (STATUS_CONFIRMADO, 'Confirmado'),
        (STATUS_EM_ANDAMENTO, 'Em andamento'),
        (STATUS_CONCLUIDO, 'Concluído'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    clientes = models.ManyToManyField(
        'Cliente', 
        through='ClienteEvento', 
        related_name='eventos'
    )
    quantidade_pessoas = models.PositiveIntegerField(
        blank=False, 
        null=False
    )
    data_hora = models.DateTimeField()
    taxa_utensilio = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    endereco = models.ForeignKey(
        Endereco, 
        related_name='eventos', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=False
    )
    tipo_evento = models.ForeignKey(
        'TipoEvento', 
        related_name='eventos', 
        on_delete=models.PROTECT, 
        null=False, 
        blank=False
    )
    equipe_evento = models.ManyToManyField(
        'Funcionario', 
        through='EquipeEvento', 
        related_name='eventos'
    )
    utensilio_evento = models.ManyToManyField(
        'Utensilio', 
        through='UtensilioEvento', 
        related_name='eventos'
    )
    local = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    taxa_deslocamento = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_CONFIRMADO
    )


    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f'{self.tipo_evento.nome} - {self.data_hora}'
