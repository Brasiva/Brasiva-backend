from django.db import models


class ClienteEvento(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cliente do Evento'
        verbose_name_plural = 'Clientes do Evento'
