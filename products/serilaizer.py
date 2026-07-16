from decimal import Decimal

from rest_framework import serializers
from .models import Collection, Product

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price','slug','inventory','price_with_tax','description','collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        raw_price_with_tax = product.unit_price * Decimal('1.1')
        return raw_price_with_tax