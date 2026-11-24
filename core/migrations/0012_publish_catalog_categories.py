from django.db import migrations, models


def hide_legacy_empty_categories(apps, schema_editor):
    Category = apps.get_model('core', 'CategoriaPrato')
    Dish = apps.get_model('core', 'Prato')
    database = schema_editor.connection.alias
    for category in Category.objects.using(database).filter(nome__in=['Entrada', 'Prato Principal', 'Sobremesa']):
        if not Dish.objects.using(database).filter(categoria_id=category.pk).exists():
            Category.objects.using(database).filter(pk=category.pk).update(publicada=False)


class Migration(migrations.Migration):
    dependencies = [('core', '0011_catalog_initial')]
    operations = [
        migrations.AddField('categoriaprato', 'publicada', models.BooleanField(default=True)),
        migrations.RunPython(hide_legacy_empty_categories, migrations.RunPython.noop),
    ]
