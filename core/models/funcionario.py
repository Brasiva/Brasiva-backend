from django.db import models

from uploader.models import Image
from phonenumber_field.modelfields import PhoneNumberField


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefone = PhoneNumberField(region='BR', blank=False)
    pagamento = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ForeignKey(
        Image,
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return self.nome
