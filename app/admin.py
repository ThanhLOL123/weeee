from typing import Any
from django.contrib import admin
from django.http import HttpRequest

# Register your models here.
from .models import Product, Category, Order, OrderItem,Payment
class ProductA(admin.ModelAdmin):
    list_display = ('photo','name','price','publisher')
    list_filter =('category',)
    search_fields =('name',)
    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('name','-price')
        return ('name',)
class CategoryA(admin.ModelAdmin):
    list_display = ('name','slug')
    list_filter =('name',)
    search_fields =('name',)
    
admin.site.register(Product,ProductA)
admin.site.register(Category,CategoryA)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)