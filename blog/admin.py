from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('author', 'status')
    list_editable = ('status',)
    search_fields = ('title', 'description')
    ordering = ('status', 'publish')
    raw_id_fields = ('author',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')
    list_filter = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'transaction_id')
    list_filter = ('customer', )


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'city', 'date_added')
    list_filter = ('customer',)


# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name', 'email')
#     list_filter = ('user',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'date_added')
    list_filter = ('product', 'order')

@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)
