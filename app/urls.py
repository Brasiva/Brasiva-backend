from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.locale import ro
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from core.views import FuncionarioViewSet, UserRegistrationView, UserViewSet, UtensilioViewSet, TipoEventoViewSet, PratoViewSet, EventoViewSet, EnderecoViewSet, CategoriaPratoViewSet, IngredienteViewSet, EstoqueViewSet, ItemCompraViewSet, CategoriaIngredienteViewSet, ClienteViewSet, OrcamentoEventoViewSet, EquipeEventoViewSet, UtensilioEventoViewSet
from uploader.router import router as uploader_router

router = DefaultRouter()

router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'categoria-pratos', CategoriaPratoViewSet, basename='categoria-pratos')
router.register(r'categoria-ingredientes', CategoriaIngredienteViewSet, basename='categoria-ingredientes')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionarios')
router.register(r'utensilios', UtensilioViewSet, basename='utensilios')
router.register(r'tipo-eventos', TipoEventoViewSet, basename='tipo-eventos')
router.register(r'pratos', PratoViewSet, basename='pratos')
router.register(r'eventos', EventoViewSet, basename='eventos')
router.register(r'enderecos', EnderecoViewSet, basename='enderecos')
router.register(r'estoque', EstoqueViewSet, basename='estoque')
router.register(r'ingredientes', IngredienteViewSet, basename='ingredientes')
router.register(r'item-compra', ItemCompraViewSet, basename='item-compra')
router.register(r'orcamento-eventos', OrcamentoEventoViewSet, basename='orcamento-eventos')
router.register(r'equipe-eventos', EquipeEventoViewSet, basename='equipe-eventos')
router.register(r'utensilio-eventos', UtensilioEventoViewSet, basename='utensilio-eventos')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/doc/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Registro de usuários
    path('api/registro/', UserRegistrationView.as_view(), name='user_registration'),
    # API
    path('api/', include(router.urls)),
    path('api/media/', include(uploader_router.urls)),
]

urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)
