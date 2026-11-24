from datetime import date, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import CategoriaPrato, Ingrediente, IngredientePrato, Notificacao, PedidoSite, Prato, User


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
        self.assertEqual(categoria['quantidade_opcoes'], 13)
        self.assertEqual(categoria['quantidade_disponiveis'], 1)

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

    def test_staff_can_login_with_email_and_access_admin_profile(self):
        response = self.client.post('/api/token/', {
            'email': 'equipe@example.test', 'password': 'senha-segura-123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        profile = self.client.get('/api/usuarios/me/')
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertTrue(profile.data['is_staff'])

    def test_staff_login_receives_site_order_and_notification(self):
        order = self.client.post('/api/pedidos-site/', self.payload(), format='json')
        self.assertEqual(order.status_code, status.HTTP_201_CREATED, order.data)
        login = self.client.post('/api/token/', {
            'email': 'equipe@example.test', 'password': 'senha-segura-123',
        }, format='json')
        self.assertEqual(login.status_code, status.HTTP_200_OK, login.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        orders = self.client.get('/api/pedidos-site/')
        notifications = self.client.get('/api/notificacoes/')
        self.assertEqual(orders.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications.status_code, status.HTTP_200_OK)
        order_rows = orders.data['results'] if 'results' in orders.data else orders.data
        notification_rows = notifications.data['results'] if 'results' in notifications.data else notifications.data
        self.assertEqual(order_rows[0]['id'], order.data['id'])
        self.assertTrue(any(row['titulo'] == 'Nova solicitação de evento' for row in notification_rows))

    def test_admin_can_open_and_save_prato_form(self):
        admin_user = User.objects.create_superuser('admin@example.test', 'senha-admin-123')
        self.client.force_login(admin_user)
        add_url = reverse('admin:core_prato_add')

        form_response = self.client.get(add_url)
        self.assertEqual(form_response.status_code, status.HTTP_200_OK)
        ingrediente = Ingrediente.objects.create(nome='Farinha de teste')

        response = self.client.post(add_url, {
            'nome': 'Prato criado pelo admin',
            'descricao': 'Cadastro pelo formulário Django Admin',
            'valor': '18.50',
            'unidade': 'unidade',
            'disponivel': 'on',
            'categoria': self.categoria.pk,
            'modo_fazer': 'Preparar e servir.',
            'ingredienteprato_set-TOTAL_FORMS': '1',
            'ingredienteprato_set-INITIAL_FORMS': '0',
            'ingredienteprato_set-MIN_NUM_FORMS': '0',
            'ingredienteprato_set-MAX_NUM_FORMS': '1000',
            'ingredienteprato_set-0-ingrediente': ingrediente.pk,
            'ingredienteprato_set-0-quantidade': '0.250',
        }, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.context)
        prato = Prato.objects.get(nome='Prato criado pelo admin', categoria=self.categoria)
        self.assertTrue(IngredientePrato.objects.filter(prato=prato, ingrediente=ingrediente, quantidade=Decimal('0.250')).exists())
