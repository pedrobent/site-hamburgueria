from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, Produto, ItemPedido, Cliente
from .serializers import PedidoSerializer
from django.contrib import messages
from .forms import ClienteForm

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def atualizar_status(self, request, pk=None):
        pedido = self.get_object()
        novo_status = request.data.get('status')
        
        if novo_status in dict(Pedido.STATUS_CHOICES):
            pedido.status = novo_status
            pedido.save()
            return Response({'status': 'success'})
        return Response({'status': 'error', 'message': 'Status inválido'}, status=400)

def pedido_list(request):
    pedidos = Pedido.objects.all().order_by('-data_criacao')
    return render(request, 'core/pedido_list.html', {'pedidos': pedidos})

def criar_pedido(request):
    return render(request, 'core/criar_pedido.html')

def lista_produtos(request):
    lanches = Produto.objects.filter(categoria='lanche', oculto=False, disponivel=True)
    bebidas = Produto.objects.filter(categoria='bebida', oculto=False, disponivel=True)
    sobremesas = Produto.objects.filter(categoria='sobremesa', oculto=False, disponivel=True)
    porcoes = Produto.objects.filter(categoria='porcao', oculto=False, disponivel=True)
    combos = Produto.objects.filter(categoria='combo', oculto=False, disponivel=True)
    pasteis = Produto.objects.filter(categoria='pastel', oculto=False, disponivel=True)
    
    context = {
        'lanches': lanches,
        'bebidas': bebidas,
        'sobremesas': sobremesas,
        'porcoes': porcoes,
        'combos': combos,
        'pasteis': pasteis,
    }
    return render(request, 'core/lista_produtos.html', context)

@csrf_exempt
def adicionar_ao_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=produto_id)
        quantidade = int(request.POST.get('quantidade', 1))
        
        if 'carrinho' not in request.session:
            request.session['carrinho'] = []
        
        carrinho = request.session['carrinho']
        
        # Verifica se o produto já está no carrinho
        item_existente = None
        for item in carrinho:
            if item['produto_id'] == produto_id:
                item['quantidade'] += quantidade
                item_existente = item
                break
        
        if not item_existente:
            carrinho.append({
                'produto_id': produto_id,
                'nome': produto.nome,
                'preco': str(produto.preco),
                'quantidade': quantidade
            })
        
        request.session.modified = True
        messages.success(request, f'{produto.nome} adicionado ao carrinho!')
        return redirect('ver_carrinho')

def ver_carrinho(request):
    carrinho = request.session.get('carrinho', [])
    total = sum(float(item['preco']) * item['quantidade'] for item in carrinho)
    return render(request, 'core/carrinho.html', {
        'carrinho': carrinho,
        'total': total
    })

def finalizar_pedido(request):
    carrinho = request.session.get('carrinho', [])
    total = sum(float(item['preco']) * item['quantidade'] for item in carrinho)
    
    if request.method == 'POST':
        if not carrinho:
            messages.error(request, 'Seu carrinho está vazio!')
            return redirect('ver_carrinho')
        
        cliente = request.POST.get('cliente')
        mesa = request.POST.get('mesa')
        observacoes = request.POST.get('observacoes')
        
        # Criar o pedido
        pedido = Pedido.objects.create(
            cliente=cliente,
            mesa=mesa,
            observacoes=observacoes
        )
        
        # Adicionar os itens do pedido
        total = 0
        for item in carrinho:
            produto = Produto.objects.get(id=item['produto_id'])
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item['quantidade'],
                preco_unitario=produto.preco
            )
            total += float(item['preco']) * item['quantidade']
        
        pedido.valor_total = total
        pedido.save()
        
        # Limpar o carrinho
        del request.session['carrinho']
        messages.success(request, f'Pedido #{pedido.numero_pedido} criado com sucesso!')
        return redirect('ver_carrinho')
    
    return render(request, 'core/finalizar_pedido.html', {
        'carrinho': carrinho,
        'total': total
    })

def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('/')
    else:
        form = ClienteForm()
    
    return render(request, 'core/cadastro_cliente.html', {'form': form})
