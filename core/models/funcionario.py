from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    pagamento = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='funcionarios/')
    def __str__(self):
        return self.nome