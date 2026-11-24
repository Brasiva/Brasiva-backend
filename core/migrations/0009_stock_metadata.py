from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0008_site_catalog_and_orders')]
    operations = [
        migrations.AddField('estoque', 'quantidade_minima', models.PositiveIntegerField(default=0)),
        migrations.AddField('ingrediente', 'valor', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
    ]
