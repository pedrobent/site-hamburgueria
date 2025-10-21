from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Pedido, Produto, ItemPedido, Cliente
from .forms import ProdutoForm

# Remover o modelo Group do admin
admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'cliente', 'mesa', 'status', 'valor_total', 'data_criacao')
    list_filter = ('status', 'data_criacao')
    search_fields = ('numero_pedido', 'cliente', 'mesa')
    inlines = [ItemPedidoInline]
    actions = ['marcar_preparando', 'marcar_finalizado']

    def marcar_preparando(self, request, queryset):
        queryset.update(status='preparando')
    marcar_preparando.short_description = "Marcar pedidos selecionados como preparando"

    def marcar_finalizado(self, request, queryset):
        queryset.update(status='finalizado')
    marcar_finalizado.short_description = "Marcar pedidos selecionados como finalizados"

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    form = ProdutoForm
    list_display = ('nome', 'categoria', 'preco', 'disponivel', 'oculto')
    list_filter = ('categoria', 'disponivel', 'oculto')
    search_fields = ('nome', 'descricao')
    actions = ['ocultar_produtos', 'reativar_produtos']
    fields = ('nome', 'descricao', 'preco', 'categoria', 'imagem', 'disponivel', 'oculto')

    def ocultar_produtos(self, request, queryset):
        queryset.update(oculto=True)
    ocultar_produtos.short_description = "Ocultar produtos selecionados"

    def reativar_produtos(self, request, queryset):
        queryset.update(oculto=False)
    reativar_produtos.short_description = "Reativar produtos selecionados"

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'data_cadastro')
    search_fields = ('nome', 'telefone', 'email')
    list_filter = ('data_cadastro',)
    fields = ('nome', 'telefone', 'email', 'endereco', 'observacoes')
