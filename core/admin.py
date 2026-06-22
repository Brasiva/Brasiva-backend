"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

from core.models import CategoriaPrato, CategoriaIngrediente, Evento, Estoque, Endereco, Funcionario, User, UserAdmin, Utensilio, TipoEvento, Prato, Ingrediente, ItemCompra, EquipeEvento, OrcamentoEvento, UtensilioEvento, IngredientePrato, PratoEvento

@register(CategoriaPrato)
class CategoriaPratoAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 10

@register(CategoriaIngrediente)
class CategoriaIngredienteAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 10

@register(Evento)
class EventoAdmin(ModelAdmin):
   # Exibe os dados reais que existem na tabela Evento
    list_display = ('id', 'data_hora', 'quantidade_pessoas', 'endereco')
    # Permite buscar pela cidade ou logradouro através da chave estrangeira (usando __)
    search_fields = ('endereco__cidade', 'endereco__logradouro')
    list_filter = ('data_hora', 'endereco__cidade')
    ordering = ('-data_hora',) # O sinal de menos (-) faz ordenar do mais recente para o mais antigo
    list_per_page = 10

@register(Endereco)
class EnderecoAdmin(ModelAdmin):
    list_display = ('logradouro', 'numero', 'bairro', 'cidade', 'estado')
    search_fields = ('logradouro', 'bairro', 'cidade')
    list_filter = ('cidade', 'estado')
    ordering = ('cidade', 'logradouro')
    list_per_page = 20