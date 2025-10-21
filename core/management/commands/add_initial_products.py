from django.core.management.base import BaseCommand
from core.models import Produto

class Command(BaseCommand):
    help = 'Adiciona os produtos iniciais ao banco de dados'

    def handle(self, *args, **kwargs):
        # Lista de produtos
        produtos = [
            {
                'nome': 'SMASH PODEROSO',
                'descricao': 'Pão especial com aquela selada crocante, mais 2 carnes de 80g cada, prensadas na chapa, acompanhadas de duas camadas generosas de molho cheddar super cremoso,ovo, bacon crocantes, alface americana, tomate e a nossa delíciosa maionese da casa...',
                'preco': 32.50,
                'categoria': 'lanche'
            },
            {
                'nome': 'BURGUER ONION BBQ',
                'descricao': 'Pão especial com aquela selada crocante, mais um delicioso hambúrguer 100% artesanal de 140g acompanhada de queijo prato,2 cebolas ONION, MOLHO BARBECUE BBQ e a nossa delíciosa maionese da casa....',
                'preco': 27.50,
                'categoria': 'lanche'
            },
            {
                'nome': 'CATU BACON',
                'descricao': 'Pão especial com aquela selada crocante, mais um delicioso hambúrguer 100% artesanal de 140g acompanhada de uma camada generosa de catupiry original aquele bacon super crocante e a nossa delíciosa maionese da casa....',
                'preco': 26.50,
                'categoria': 'lanche'
            },
            {
                'nome': 'Coca cola 600ml',
                'descricao': 'Coca cola 600ml',
                'preco': 8.00,
                'categoria': 'bebida'
            },
            {
                'nome': 'Guaraná 600ml',
                'descricao': 'Guaraná 600ml',
                'preco': 8.00,
                'categoria': 'bebida'
            },
            {
                'nome': 'Coca cola 350ml',
                'descricao': 'Coca cola 350ml',
                'preco': 6.00,
                'categoria': 'bebida'
            },
            {
                'nome': 'Guaraná 350ml',
                'descricao': 'Guaraná 350ml',
                'preco': 6.00,
                'categoria': 'bebida'
            },
            # Novos produtos - Sobremesas
            {
                'nome': 'Pudim de Leite',
                'descricao': 'Pudim de leite condensado com calda de caramelo',
                'preco': 8.50,
                'categoria': 'sobremesa'
            },
            {
                'nome': 'Mousse de Chocolate',
                'descricao': 'Mousse de chocolate com raspas de chocolate',
                'preco': 9.00,
                'categoria': 'sobremesa'
            },
            {
                'nome': 'Sorvete de Baunilha',
                'descricao': 'Sorvete de baunilha com calda de chocolate',
                'preco': 7.50,
                'categoria': 'sobremesa'
            },
            # Novos produtos - Porções
            {
                'nome': 'Batata Frita',
                'descricao': 'Porção de batata frita crocante',
                'preco': 15.00,
                'categoria': 'porcao'
            },
            {
                'nome': 'Onion Rings',
                'descricao': 'Porção de anéis de cebola empanados e fritos',
                'preco': 18.00,
                'categoria': 'porcao'
            },
            {
                'nome': 'Nuggets de Frango',
                'descricao': 'Porção de nuggets de frango com molho barbecue',
                'preco': 20.00,
                'categoria': 'porcao'
            },
            # Novos produtos - Combos
            {
                'nome': 'Combo Duplo',
                'descricao': '2 lanches + 2 bebidas 350ml',
                'preco': 45.00,
                'categoria': 'combo'
            },
            {
                'nome': 'Combo Família',
                'descricao': '4 lanches + 4 bebidas 600ml + 1 porção grande',
                'preco': 95.00,
                'categoria': 'combo'
            },
            {
                'nome': 'Combo Individual',
                'descricao': '1 lanche + 1 bebida 350ml + 1 sobremesa',
                'preco': 25.00,
                'categoria': 'combo'
            },
        ]

        for produto_data in produtos:
            produto, created = Produto.objects.get_or_create(
                nome=produto_data['nome'],
                defaults={
                    'descricao': produto_data['descricao'],
                    'preco': produto_data['preco'],
                    'categoria': produto_data['categoria']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Produto "{produto.nome}" criado com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING(f'Produto "{produto.nome}" já existe.')) 