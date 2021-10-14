from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('author', 'status')
    list_editable = ('status',)
    search_fields = ('title', 'description')
    ordering = ('status', 'publish')
    raw_id_fields = ('author',)
    prepopulated_fields = {"slug": ("title",)}

