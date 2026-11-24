from django.db import migrations, models


def add_metadata_columns_if_missing(apps, schema_editor):
    connection = schema_editor.connection
    fields = [
        ('estoque', 'quantidade_minima', models.PositiveIntegerField(default=0)),
        ('ingrediente', 'valor', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
    ]
    with connection.cursor() as cursor:
        tables = set(connection.introspection.table_names(cursor))
        for model_name, field_name, field in fields:
            Model = apps.get_model('core', model_name)
            table = Model._meta.db_table
            if table not in tables:
                raise RuntimeError(f'Required table {table} is missing while applying catalog metadata.')
            columns = {
                column.name
                for column in connection.introspection.get_table_description(cursor, table)
            }
            if field_name not in columns:
                column_sql = f'{schema_editor.quote_name(field_name)} {field.db_type(connection)} NOT NULL'
                if field.has_default():
                    column_sql += f' DEFAULT {schema_editor.quote_value(field.get_default())}'
                schema_editor.execute(
                    f'ALTER TABLE {schema_editor.quote_name(table)} ADD COLUMN {column_sql}'
                )


class Migration(migrations.Migration):
    initial = True
    dependencies = [('core', '0008_site_catalog_and_orders')]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_metadata_columns_if_missing, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField('estoque', 'quantidade_minima', models.PositiveIntegerField(default=0)),
                migrations.AddField('ingrediente', 'valor', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
