from django.contrib import admin
from .models import Category , Products
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug' , 'name']
    search_fields = ['name']
    readonly_fields = ['slug']
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description' , 'price']
    search_fields = ['name']
    readonly_fields = ['slug']