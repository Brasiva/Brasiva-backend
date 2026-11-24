import unicodedata
from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


CATALOG = [
    ('Salgados tradicionais', 'cento (100 unidades)', [
        ('Coxinha de frango', '95.00'), ('Bolinha de queijo', '90.00'), ('Risole de presunto e queijo', '90.00'), ('Risole de carne', '95.00'), ('Quibe tradicional', '95.00'), ('Enroladinho de salsicha', '85.00'), ('Croquete de carne', '100.00'), ('Bolinho de aipim com carne', '110.00'), ('Empadinha de frango', '120.00'), ('Esfiha de carne', '110.00'), ('Pastelzinho de queijo', '95.00'), ('Pastelzinho de carne', '100.00'),
    ]),
    ('Salgados especiais e finos', 'cento (100 unidades)', [
        ('Camarão empanado', '220.00'), ('Mini quiche de alho-poró', '160.00'), ('Mini quiche de queijo', '150.00'), ('Canudinho de frango', '130.00'), ('Barquete de salpicão', '160.00'), ('Trouxinha de frango', '145.00'), ('Folhado de queijo', '160.00'), ('Folhado de presunto e queijo', '165.00'), ('Mini empada de camarão', '220.00'), ('Mini pastel de camarão', '210.00'),
    ]),
    ('Docinhos tradicionais', 'cento (100 unidades)', [
        ('Brigadeiro tradicional', '110.00'), ('Beijinho', '105.00'), ('Cajuzinho', '110.00'), ('Bicho-de-pé', '110.00'), ('Olho-de-sogra', '125.00'), ('Casadinho', '120.00'), ('Dois amores', '120.00'), ('Ninho tradicional', '125.00'), ('Brigadeiro branco', '120.00'), ('Amendoim doce', '110.00'),
    ]),
    ('Docinhos gourmet', 'cento (100 unidades)', [
        ('Brigadeiro de pistache', '220.00'), ('Brigadeiro de Nutella', '200.00'), ('Brigadeiro de Oreo', '180.00'), ('Brigadeiro de churros', '170.00'), ('Brigadeiro de paçoca', '160.00'), ('Ninho com Nutella', '190.00'), ('Trufa de chocolate', '180.00'), ('Camafeu de nozes', '230.00'), ('Copinho de chocolate', '190.00'), ('Mini brownie', '180.00'),
    ]),
    ('Pratos principais', 'por pessoa', [
        ('Strogonoff de frango', '32.00'), ('Strogonoff de carne', '39.00'), ('Fricassê de frango', '35.00'), ('Lasanha à bolonhesa', '38.00'), ('Lasanha de frango', '35.00'), ('Escondidinho de carne', '36.00'), ('Escondidinho de frango', '33.00'), ('Frango ao molho branco', '36.00'), ('Carne assada ao molho madeira', '48.00'), ('Filé de frango grelhado', '32.00'), ('Filé de peixe ao molho', '42.00'), ('Pernil assado', '39.00'), ('Medalhão de frango', '42.00'), ('Risoto de frango', '38.00'), ('Risoto de camarão', '55.00'),
    ]),
    ('Acompanhamentos', 'kg', [
        ('Arroz branco', '25.00'), ('Arroz à grega', '35.00'), ('Arroz com brócolis', '32.00'), ('Arroz carreteiro', '42.00'), ('Purê de batata', '30.00'), ('Batata gratinada', '42.00'), ('Batata rústica', '35.00'), ('Farofa especial', '32.00'), ('Macarrão ao molho branco', '35.00'), ('Macarrão à bolonhesa', '38.00'), ('Legumes salteados', '35.00'), ('Polenta cremosa', '28.00'),
    ]),
    ('Saladas', 'kg', [
        ('Salada tropical', '42.00'), ('Salada Caesar', '48.00'), ('Salada de maionese', '35.00'), ('Salpicão de frango', '45.00'), ('Salada de folhas verdes', '32.00'), ('Salada de legumes', '35.00'), ('Salada de macarrão', '38.00'), ('Vinagrete', '25.00'),
    ]),
    ('Sobremesas', 'kg', [
        ('Mousse de chocolate', '55.00'), ('Mousse de maracujá', '50.00'), ('Pavê de chocolate', '60.00'), ('Pavê de limão', '55.00'), ('Pudim de leite condensado', '65.00'), ('Manjar de coco', '55.00'), ('Torta de limão', '70.00'), ('Gelatina colorida', '35.00'), ('Copinho de sobremesa', '7.00', 'unidade'), ('Mini cheesecake', '9.00', 'unidade'),
    ]),
    ('Bolos e tortas', 'kg', [
        ('Bolo de chocolate', '65.00'), ('Bolo de brigadeiro', '75.00'), ('Bolo de ninho', '80.00'), ('Bolo de cenoura com chocolate', '65.00'), ('Bolo de prestígio', '75.00'), ('Bolo de morango', '85.00'), ('Bolo de abacaxi', '75.00'), ('Bolo de doce de leite', '80.00'), ('Bolo de aniversário decorado', '95.00'), ('Torta de limão', '70.00'), ('Torta holandesa', '85.00'), ('Torta de morango', '85.00'), ('Torta de maracujá', '75.00'), ('Naked cake', '110.00'),
    ]),
    ('Bebidas', 'unidade', [
        ('Água mineral', '3.50', '500 ml'), ('Água com gás', '4.50', '500 ml'), ('Refrigerante', '12.00', '2 litros'), ('Refrigerante lata', '5.00', '350 ml'), ('Suco natural de laranja', '15.00', '1 litro'), ('Suco natural de uva', '16.00', '1 litro'), ('Suco de maracujá', '14.00', '1 litro'), ('Suco de limão', '12.00', '1 litro'), ('Chá gelado', '12.00', '1 litro'),
    ]),
    ('Lanches e finger foods', 'unidade', [
        ('Mini hambúrguer', '7.00'), ('Mini cachorro-quente', '6.00'), ('Mini pizza', '6.50'), ('Mini sanduíche natural', '7.00'), ('Wrap de frango', '9.00'), ('Barquinha de frango', '6.00'), ('Mini hot dog gourmet', '8.00'), ('Tábua de frios', '120.00', 'porção'), ('Mini bruschetta', '6.00'), ('Espetinho caprese', '7.00'),
    ]),
    ('Serviços adicionais', 'evento', [
        ('Garçom', '180.00', 'diária'), ('Copeira', '170.00', 'diária'), ('Churrasqueiro', '250.00', 'diária'), ('Equipe de cozinha', '300.00', 'diária'), ('Montagem de mesa', '150.00', 'evento'), ('Decoração simples', '250.00', 'evento'), ('Decoração personalizada', None, 'sob orçamento'), ('Aluguel de pratos e talheres', '5.00', 'por pessoa'), ('Aluguel de copos', '3.00', 'por pessoa'), ('Aluguel de toalhas', '15.00', 'unidade'), ('Entrega', '15.00', 'por pedido'),
    ]),
]


def normalize(value):
    return unicodedata.normalize('NFKC', value).strip().casefold()


def seed_catalog(apps, schema_editor):
    Category = apps.get_model('core', 'CategoriaPrato')
    Dish = apps.get_model('core', 'Prato')
    database = schema_editor.connection.alias
    categories = {normalize(item.nome): item for item in Category.objects.using(database).all()}
    for name, default_unit, products in CATALOG:
        key = normalize(name)
        category = categories.get(key)
        if category is None:
            category = Category.objects.using(database).create(nome=name)
            categories[key] = category
        existing = {normalize(item.nome) for item in Dish.objects.using(database).filter(categoria_id=category.pk)}
        for product in products:
            product_name, price, *specific_unit = product
            if normalize(product_name) in existing:
                continue
            quote_only = price is None
            Dish.objects.using(database).create(
                nome=product_name,
                descricao='Valor inicial sugerido; confirmar condições com a equipe Brasiva.' if product_name == 'Entrega' else '',
                valor=Decimal(price) if price is not None else None,
                categoria_id=category.pk,
                unidade=specific_unit[0] if specific_unit else default_unit,
                disponivel=False,
                sob_orcamento=quote_only,
                imagem=None,
            )
            existing.add(normalize(product_name))


class Migration(migrations.Migration):
    dependencies = [('core', '0010_notificacao')]

    operations = [
        migrations.AddField('prato', 'sob_orcamento', models.BooleanField(default=False)),
        migrations.AddField('prato', 'imagem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pratos', to='uploader.image')),
        migrations.AddField('prato', 'criado_em', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now), preserve_default=False),
        migrations.AddField('prato', 'atualizado_em', models.DateTimeField(auto_now=True, default=django.utils.timezone.now), preserve_default=False),
        migrations.RunPython(seed_catalog, migrations.RunPython.noop),
    ]
