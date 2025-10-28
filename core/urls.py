from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import (
    PedidoViewSet, lista_produtos, adicionar_ao_carrinho,
    ver_carrinho, finalizar_pedido, pedido_list, criar_pedido, cadastro_cliente
)

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('lista de produtos/', lista_produtos, name='lista_produtos'),
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/finalizar/', finalizar_pedido, name='finalizar_pedido'),
    path('pedidos/', pedido_list, name='pedido_list'),
    path('criar-pedido/', criar_pedido, name='criar_pedido'),
    path('cadastro-cliente/', cadastro_cliente, name='cadastro_cliente'),
] 