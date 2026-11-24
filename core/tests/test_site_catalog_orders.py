from datetime import date, timedelta
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import CategoriaPrato, Notificacao, PedidoSite, Prato, User


class SiteCatalogAndOrdersTests(APITestCase):
    def setUp(self):
        self.categoria = CategoriaPrato.objects.get(nome='Salgados tradicionais')
        self.prato = Prato.objects.create(
            nome='Coxinha de teste', descricao='Recheio de frango', valor=Decimal('2.50'),
            unidade='unidade', disponivel=True, sob_orcamento=False, categoria=self.categoria,
        )
        self.staff = User.objects.create_user('equipe@example.test', 'senha-segura-123', is_staff=True)

    def payload(self):
        return {
            'nome': 'Cliente de teste', 'email': 'cliente@example.test', 'telefone': '+5511999999999',
            'tipo_evento': 'Aniversário', 'data_evento': (date.today() + timedelta(days=30)).isoformat(),
            'convidados': 20, 'observacoes': 'Teste de integração',
            'itens': [{'prato': self.prato.pk, 'quantidade': 10}],
        }

    def test_01_categories_are_public_and_show_live_count(self):
        response = self.client.get('/api/categoria-pratos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = response.data['results'] if 'results' in response.data else response.data
        for page in range(2, response.data.get('total_pages', 1) + 1):
            rows.extend(self.client.get('/api/categoria-pratos/', {'page': page}).data['results'])
        categoria = next(row for row in rows if row['id'] == self.categoria.pk)
        self.assertEqual(categoria['quantidade_opcoes'], 1)

    def test_02_products_are_public_and_filter_by_category(self):
        response = self.client.get('/api/pratos/', {'categoria': self.categoria.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual([row['id'] for row in rows], [self.prato.pk])

    def test_03_staff_price_changes_are_reflected_in_public_catalog(self):
        self.client.force_authenticate(self.staff)
        updated = self.client.patch(f'/api/pratos/{self.prato.pk}/', {'valor': '3.75'}, format='json')
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(None)
        public = self.client.get(f'/api/pratos/{self.prato.pk}/')
        self.assertEqual(str(public.data['valor']), '3.75')

    def test_04_unavailable_products_are_not_selectable_publicly(self):
        self.client.force_authenticate(self.staff)
        self.client.patch(f'/api/pratos/{self.prato.pk}/', {'disponivel': False}, format='json')
        self.client.force_authenticate(None)
        response = self.client.get('/api/pratos/')
        rows = response.data['results'] if 'results' in response.data else response.data
        self.assertNotIn(self.prato.pk, [row['id'] for row in rows])

    def test_05_order_uses_database_prices_and_persists(self):
        payload = self.payload()
        payload['total_estimado'] = '0.01'
        response = self.client.post('/api/pedidos-site/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        pedido = PedidoSite.objects.get(pk=response.data['id'])
        self.assertEqual(pedido.total_estimado, Decimal('25.00'))
        self.assertEqual(pedido.status, 'novo')

    def test_06_staff_can_receive_submitted_orders(self):
        self.client.post('/api/pedidos-site/', self.payload(), format='json')
        self.client.force_authenticate(self.staff)
        response = self.client.get('/api/pedidos-site/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(rows[0]['email'], 'cliente@example.test')

    def test_07_staff_status_updates_are_persisted(self):
        created = self.client.post('/api/pedidos-site/', self.payload(), format='json')
        self.client.force_authenticate(self.staff)
        changed = self.client.patch(f"/api/pedidos-site/{created.data['id']}/", {'status': 'em_analise'}, format='json')
        self.assertEqual(changed.status_code, status.HTTP_200_OK)
        self.assertEqual(PedidoSite.objects.get(pk=created.data['id']).status, 'em_analise')

    def test_08_order_details_are_private(self):
        self.client.post('/api/pedidos-site/', self.payload(), format='json')
        self.assertEqual(self.client.get('/api/pedidos-site/').status_code, status.HTTP_401_UNAUTHORIZED)

    def test_09_only_staff_can_change_catalog(self):
        self.assertEqual(self.client.post('/api/pratos/', {'nome': 'Novo', 'categoria': self.categoria.pk}, format='json').status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(User.objects.create_user('cliente2@example.test', 'senha-segura-456'))
        self.assertEqual(self.client.post('/api/categoria-pratos/', {'nome': 'Sem permissão'}, format='json').status_code, status.HTTP_403_FORBIDDEN)

    def test_10_new_order_creates_staff_notification(self):
        self.client.post('/api/pedidos-site/', self.payload(), format='json')
        self.assertTrue(Notificacao.objects.filter(usuario=self.staff, titulo='Nova solicitação de evento').exists())

    def test_quote_only_product_is_selectable_without_invented_price(self):
        self.prato.valor = None
        self.prato.sob_orcamento = True
        self.prato.save()
        response = self.client.post('/api/pedidos-site/', self.payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        pedido = PedidoSite.objects.get(pk=response.data['id'])
        self.assertEqual(pedido.total_estimado, Decimal('0.00'))
        self.assertIsNone(pedido.itens[0]['valor_unitario'])
        self.assertTrue(pedido.itens[0]['sob_orcamento'])

    def test_catalog_seed_contains_all_requested_sections_and_items(self):
        sections = {
            'Salgados tradicionais', 'Salgados especiais e finos', 'Docinhos tradicionais', 'Docinhos gourmet',
            'Pratos principais', 'Acompanhamentos', 'Saladas', 'Sobremesas', 'Bolos e tortas', 'Bebidas',
            'Lanches e finger foods', 'Serviços adicionais',
        }
        stored = set(CategoriaPrato.objects.filter(nome__in=sections).values_list('nome', flat=True))
        self.assertEqual(stored, sections)
        self.assertEqual(Prato.objects.filter(categoria__nome__in=sections).exclude(nome='Coxinha de teste').count(), 131)
        self.assertEqual(Prato.objects.filter(categoria__nome__in=sections, disponivel=True).exclude(nome='Coxinha de teste').count(), 0)

    def test_public_menu_contains_exactly_the_twelve_requested_categories(self):
        response = self.client.get('/api/categoria-pratos/')
        rows = response.data['results'] if 'results' in response.data else response.data
        for page in range(2, response.data.get('total_pages', 1) + 1):
            next_page = self.client.get('/api/categoria-pratos/', {'page': page})
            rows.extend(next_page.data['results'])
        names = {item['nome'] for item in rows}
        self.assertEqual(len(names), 12)
        self.assertIn('Serviços adicionais', names)
