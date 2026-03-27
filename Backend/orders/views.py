from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .utils import send_order_notification

# Create your views here.
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated,]     # The user must be logged in

    def post(self, request):
        cart = Cart.objects.get(user=request.user)      # Get the user's cart
        shipping_address = request.data.get('shippingAddress')
        if not cart or cart.items.count() == 0:     # Check if cart is empty
            return Response({'error': 'The cart is empty.'})
        # Create order
        order = Order.objects.create(
            user=request.user,
            subtotal=cart.subtotal,
            tax_amount=cart.tax_amount,
            grand_total=cart.grand_total,
            address=shipping_address.get('address'),
            phone_number=shipping_address.get('phone_number'),
            city=shipping_address.get('city'),
            state=shipping_address.get('state'),
            postal_code=shipping_address.get('postal_code')
        )
        # Loop through cart items
        for item in cart.items.all():
            product = item.product
            # Check quantity
            if product.stock < item.quantity:
                return Response({'details': f'Only {product.stock} {product.name} are in stock.'}, status=status.HTTP_400_BAD_REQUEST)
            # Change the product stock
            product.stock -= item.quantity
            product.save()
        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.total_price
            )
        # Clear cart items
        cart.items.all().delete()
        cart.save()
        # Send notification email
        send_order_notification(order)
        # Send response to frontend
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyOrderView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk, user=self.request.user)
        return order