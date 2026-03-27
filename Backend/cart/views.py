from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer
from products.models import Product

# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        if not product_id:
            return Response({'error': 'product_id is required.'})
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if 'change' not in request.data:
            return Response({'error': 'Provide "change" field.'})
        
        change = int(request.data.get('change'))
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        product = cart_item.product
        if change > 0:
            if cart_item.quantity + change > product.stock:
                return Response({'error': 'Not enough stock.'})
            
        new_quantity = cart_item.quantity + change
        if new_quantity <= 0:
            cart_item.delete()
            return Response({'info': 'Cart item removed.'})
        
        cart_item.quantity = new_quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)