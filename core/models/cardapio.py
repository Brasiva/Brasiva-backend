from django.db import models


class Cardapio(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Cardápio')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='cardapios')
    # Aqui vinculamos o Cardapio aos pratos que foram selecionados para o Evento
    pratos = models.ManyToManyField('Prato', blank=True)

    class Meta:
        verbose_name = 'Cardápio'
        verbose_name_plural = 'Cardápios'

    def __str__(self):
        return f'Cardápio {self.nome} - {self.evento}'
