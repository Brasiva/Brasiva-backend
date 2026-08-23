from django.db import models


class Convite(models.Model):
    """Convite para ativação de acesso de funcionário."""

    token_hash = models.CharField(max_length=255)
    expira_em = models.DateTimeField()
    usado = models.BooleanField(default=False)
    funcionario = models.ForeignKey(
        'core.Funcionario',
        related_name='convites',
        on_delete=models.CASCADE,
    )
    grupo = models.ForeignKey(
        'auth.Group',
        on_delete=models.PROTECT,
    )
    criado_por = models.ForeignKey(
        'core.User',
        related_name='convites_criados',
        on_delete=models.PROTECT,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Convite'
        verbose_name_plural = 'Convites'