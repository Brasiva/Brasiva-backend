from django.db import models
from .endereco import Endereco


class Evento(models.Model):
    cliente = models.ForeignKey('Cliente', related_name='eventos', on_delete=models.SET_NULL, null=True, blank=False)
    quantidade_pessoas = models.PositiveIntegerField(blank=False, null=False)
    data_hora = models.DateTimeField()
    taxa_utensilio = models.DecimalField(max_digits=10, decimal_places=2)
    endereco = models.ForeignKey(Endereco, related_name='eventos', on_delete=models.SET_NULL, null=True, blank=False)
    tipo_evento = models.ForeignKey('TipoEvento', related_name='eventos', on_delete=models.SET_NULL, null=True, blank=False)
    equipe_evento = models.ManyToManyField('Funcionario', through='EquipeEvento', related_name='eventos')
    utensilio_evento = models.ManyToManyField('Utensilio', through='UtensilioEvento', related_name='eventos')
    prato_evento = models.ManyToManyField('Prato', through='PratoEvento', related_name='eventos')

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f'Evento {self.id} - {self.endereco.logradouro if self.endereco else "Sem endereço"}'
