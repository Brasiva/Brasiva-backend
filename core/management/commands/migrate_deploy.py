import importlib
import importlib
from types import SimpleNamespace

from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.db import connection


def core_schema_matches_models():
    with connection.cursor() as cursor:
        tables = set(connection.introspection.table_names(cursor))
        for Model in apps.get_app_config('core').get_models():
            table = Model._meta.db_table
            if table not in tables:
                return False
            columns = {
                column.name
                for column in connection.introspection.get_table_description(cursor, table)
            }
            if any(field.column not in columns for field in Model._meta.local_fields):
                return False
    return True


def hide_legacy_empty_categories():
    Category = apps.get_model('core', 'CategoriaPrato')
    Dish = apps.get_model('core', 'Prato')
    for category in Category.objects.filter(nome__in=['Entrada', 'Prato Principal', 'Sobremesa']):
        if not Dish.objects.filter(categoria_id=category.pk).exists():
            Category.objects.filter(pk=category.pk).update(publicada=False)


class Command(BaseCommand):
    help = 'Run database migrations, reconciling legacy migration records when the schema is already current.'

    def handle(self, *args, **options):
        if core_schema_matches_models():
            self.stdout.write('Existing core schema matches the current models; recording its migrations without recreating tables.')
            call_command('migrate', 'core', fake=True, interactive=False)
            call_command('migrate', fake_initial=True, interactive=False)
        else:
            call_command('migrate', fake_initial=True, interactive=False)

        # Initial migrations may be faked when their tables already exist. The
        # seed is idempotent, so run it afterward to fill any missing catalog rows.
        migration = importlib.import_module('core.migrations.0011_catalog_initial')
        migration.seed_catalog(apps, SimpleNamespace(connection=connection))
        hide_legacy_empty_categories()
