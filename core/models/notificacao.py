from django.conf import settings
from django.db import models


class Notificacao(models.Model):
    TIPOS = [('info', 'Informação'), ('sucesso', 'Sucesso'), ('alerta', 'Alerta'), ('erro', 'Erro')]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes')
    titulo = models.CharField(max_length=120)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPOS, default='info')
    lida = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.titulo
