from rest_framework import serializers
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'numero_pedido', 'cliente', 'mesa', 'itens', 'valor_total', 'observacoes', 'status', 'data_criacao', 'data_atualizacao']
        read_only_fields = ['numero_pedido', 'data_criacao', 'data_atualizacao']

    def create(self, validated_data):
        return Pedido.objects.create(**validated_data) 