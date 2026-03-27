from rest_framework import serializers

from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True)
    tax_percent = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.tax_percent', read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    subtotal = serializers.ReadOnlyField()
    grand_total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = '__all__'