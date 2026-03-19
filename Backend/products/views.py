from rest_framework import generics

from django.shortcuts import render

from .models import Product
from .serializers import ProductSerializer

# Create your views here.
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer