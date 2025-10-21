from django.db import models
from django.utils.text import slugify
import os

def get_upload_path(instance, filename):
    # Gera um nome de arquivo único baseado no nome do produto
    name, ext = os.path.splitext(filename)
    slug = slugify(instance.nome)
    return f'produtos/{slug}{ext}'

class Produto(models.Model):
    CATEGORIAS = [
        ('lanche', 'Lanche'),
        ('bebida', 'Bebida'),
        ('sobremesa', 'Sobremesa'),
        ('porcao', 'Porção'),
        ('combo', 'Combo'),
        ('pastel', 'Pastel'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    oculto = models.BooleanField(default=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    imagem = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['categoria', 'nome']

    def save(self, *args, **kwargs):
        # Se o produto já existe e a imagem foi alterada
        if self.pk:
            try:
                old_instance = Produto.objects.get(pk=self.pk)
                if old_instance.imagem and old_instance.imagem != self.imagem:
                    # Remove a imagem antiga
                    old_instance.imagem.delete(save=False)
            except Produto.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove a imagem ao deletar o produto
        if self.imagem:
            self.imagem.delete(save=False)
        super().delete(*args, **kwargs)

class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='itens_pedido')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    class Meta:
        ordering = ['pedido', 'produto']

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('finalizado', 'Finalizado'),
    ]

    numero_pedido = models.CharField(max_length=50, unique=True, editable=False)
    cliente = models.CharField(max_length=100)
    mesa = models.CharField(max_length=10, blank=True, null=True)
    itens = models.TextField()
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            # Pega o último pedido
            ultimo_pedido = Pedido.objects.order_by('-id').first()
            if ultimo_pedido:
                # Extrai o número do último pedido e incrementa
                ultimo_numero = int(ultimo_pedido.numero_pedido.split('-')[1])
                self.numero_pedido = f'PED-{ultimo_numero + 1:04d}'
            else:
                # Se for o primeiro pedido
                self.numero_pedido = 'PED-0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.numero_pedido} - {self.cliente}"

    class Meta:
        ordering = ['-data_criacao']

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    class Meta:
        ordering = ['nome', 'sobrenome']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
