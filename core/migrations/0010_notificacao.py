from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_stock_metadata'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [migrations.CreateModel(
        name='Notificacao',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('titulo', models.CharField(max_length=120)),
            ('mensagem', models.TextField()),
            ('tipo', models.CharField(choices=[('info', 'Informação'), ('sucesso', 'Sucesso'), ('alerta', 'Alerta'), ('erro', 'Erro')], default='info', max_length=10)),
            ('lida', models.BooleanField(default=False)),
            ('data', models.DateTimeField(auto_now_add=True)),
            ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes', to=settings.AUTH_USER_MODEL)),
        ],
        options={'ordering': ['-data']},
    )]
