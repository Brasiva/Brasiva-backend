"""
Django admin customization.
"""

from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import (
    CategoriaIngrediente,
    CategoriaPrato,
    CardapioEvento,
    Convite,
    Compra,
    Cliente,
    ClienteEvento,
    Endereco,
    EquipeEvento,
    Estoque,
    Evento,
    Funcionario,
    Ingrediente,
    IngredientePrato,
    ItemCompra,
    Prato,
    TipoEvento,
    User,
    Utensilio,
    UtensilioEvento,
    OrcamentoEvento,
)


@register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'foto')}),# inclua a foto aqui
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


@register(CardapioEvento)
class CardapioEventoAdmin(ModelAdmin):
    list_display = ('id', 'evento', 'prato')
    search_fields = ('prato__nome',)
    list_filter = ('evento',)
    list_per_page = 10

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

@register(Convite)
class ConviteAdmin(ModelAdmin):
    list_display = ('funcionario', 'grupo', 'usado', 'expira_em', 'criado_por')
    search_fields = ('funcionario__nome',)
    list_filter = ('usado', 'grupo')
    ordering = ('-criado_em',)
    list_per_page = 20

@register(Compra)
class CompraAdmin(ModelAdmin):
    list_display = ('id', 'evento', 'data_compra', 'valor', 'status')
    list_filter = ('status',)
    ordering = ('-data_compra',)
    list_per_page = 20

@register(ClienteEvento)
class ClienteEventoAdmin(ModelAdmin):
    list_display = ('cliente', 'evento')
    search_fields = ('cliente__nome', 'evento__id')
    list_filter = ('evento',)
    list_per_page = 20

@register(Endereco)
class EnderecoAdmin(ModelAdmin):
    list_display = ('logradouro', 'numero', 'cidade', 'estado')
    search_fields = ('logradouro', 'cidade', 'bairro')
    list_filter = ('cidade', 'estado')
    ordering = ('cidade',)
    list_per_page = 20

@register(Evento)
class EventoAdmin(ModelAdmin):
   # Exibe os dados reais que existem na tabela Evento
    list_display = ('id', 'data_hora', 'quantidade_pessoas', 'endereco', 'status')
    # Permite buscar pela cidade ou logradouro através da chave estrangeira (usando __)
    search_fields = ('endereco__cidade', 'endereco__logradouro',)
    list_filter = ('data_hora', 'endereco__cidade', 'status') # Permite filtrar por data, cidade e status
    ordering = ('-data_hora',) # O sinal de menos (-) faz ordenar do mais recente para o mais antigo
    list_per_page = 10

@register(Estoque)
class EstoqueAdmin(ModelAdmin):
    # Exibe o id, a quantidade atual e a unidade de medida em colunas separadas
    list_display = ('id', 'quantidade', 'und_medida')
    # Cria um filtro lateral para separar por unidade de medida (ex: ver só o que é KG)
    list_filter = ('und_medida',)
    # Ordena os itens em ordem alfabética pelo id
    ordering = ('id',)
    # Mostra 20 itens por página
    list_per_page = 20

@register(Funcionario)
class FuncionarioAdmin(ModelAdmin):
    list_display = ('nome', 'cargo', 'pagamento')
    search_fields = ('nome', 'cargo')
    list_filter = ('cargo',)
    ordering = ('nome',)
    list_per_page = 15

@register(Utensilio)
class UtensilioAdmin(ModelAdmin):
    list_display = ('nome', 'quantidade', 'material')
    search_fields = ('nome', 'material')
    list_filter = ('material',)
    ordering = ('nome',)
    list_per_page = 20

@register(TipoEvento)
class TipoEventoAdmin(ModelAdmin):
    list_display = ('nome', 'cor')
    search_fields = ('nome',)
    ordering = ('nome',)
    list_per_page = 10

@register(Prato)
class PratoAdmin(ModelAdmin):
    list_display = ('nome', 'valor', 'categoria')
    search_fields = ('nome', 'categoria__nome')
    list_filter = ('categoria',)
    ordering = ('nome',)
    list_per_page = 15

@register(Ingrediente)
class IngredienteAdmin(ModelAdmin):
    list_display = ('nome', 'categoria_ingrediente', 'estoque')
    search_fields = ('nome',)
    list_filter = ('categoria_ingrediente',)
    ordering = ('nome',)
    list_per_page = 20

@register(ItemCompra)
class ItemCompraAdmin(ModelAdmin):
    list_display = ('id', 'compra', 'ingrediente', 'nome', 'quantidade')
    search_fields = ('nome', 'ingrediente__nome')
    list_filter = ('compra',)
    list_per_page = 20

@register(EquipeEvento)
class EquipeEventoAdmin(ModelAdmin):
    list_display = ('funcionario', 'evento')
    search_fields = ('funcionario__nome', 'evento__id')
    list_filter = ('evento', 'funcionario')
    list_per_page = 20

@register(UtensilioEvento)
class UtensilioEventoAdmin(ModelAdmin):
    list_display = ('utensilio', 'evento')
    search_fields = ('utensilio__nome', 'evento__id')
    list_filter = ('evento', 'utensilio')
    list_per_page = 20

@register(IngredientePrato)
class IngredientePratoAdmin(ModelAdmin):
    list_display = ('prato', 'ingrediente')
    search_fields = ('prato__nome', 'ingrediente__nome')
    list_filter = ('prato', 'ingrediente')
    ordering = ('prato__nome',)
    list_per_page = 20

@register(OrcamentoEvento)
class OrcamentoEventoAdmin(ModelAdmin):
    list_display = ('evento', 'mao_de_obra', 'valor_total', 'status')
    search_fields = ('evento__id',)
    list_per_page = 20

@register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email', 'telefone')
    ordering = ('nome',)
    list_per_page = 20