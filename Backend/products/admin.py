from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'stock', 'tax_percent', 'is_active']
    ordering = ['name']


# Register your models here.
admin.site.register(Product, ProductAdmin)