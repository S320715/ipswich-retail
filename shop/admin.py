"""Admin configuration for the shop application."""

from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'age_range', 'featured', 'created_at']
    list_filter = ['category', 'age_range', 'featured']
    search_fields = ['name', 'description']
    list_editable = ['price', 'featured']
    ordering = ['-created_at']
