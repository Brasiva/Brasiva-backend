from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0007_prato_modo_fazer')]

    operations = [
        migrations.AddField('prato', 'descricao', models.TextField(blank=True, default='')),
        migrations.AddField('prato', 'unidade', models.CharField(blank=True, default='unidade', max_length=30)),
        migrations.AddField('prato', 'disponivel', models.BooleanField(default=True)),
        migrations.CreateModel(
            name='PedidoSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=30)),
                ('tipo_evento', models.CharField(max_length=100)),
                ('data_evento', models.DateField()),
                ('convidados', models.PositiveIntegerField()),
                ('observacoes', models.TextField(blank=True, default='')),
                ('itens', models.JSONField(default=list)),
                ('total_estimado', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('novo', 'Novo'), ('em_analise', 'Em análise'), ('contatado', 'Contatado'), ('aprovado', 'Aprovado'), ('recusado', 'Recusado')], default='novo', max_length=20)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-criado_em']},
        ),
    ]
