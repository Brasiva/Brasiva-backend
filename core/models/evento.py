from django.db import models


class Endereco(models.Model):
    logradouro = models.CharField(max_length=255) # Rua, Av, etc.
    numero = models.PositiveIntegerField(blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2) # UF
    cep = models.PositiveIntegerField(verbose_name='CEP', blank=True, null=True) 
    complemento = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"


class Evento(models.Model):
    quantidade_pessoas = models.PositiveIntegerField(blank=False, null=False)
    endereco = models.ForeignKey(
        'Endereco',
        related_name='eventos',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
    )
    data_hora = models.DateTimeField()
    taxa_utensilio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.endereco.logradouro if self.endereco else "Evento sem endereço"
