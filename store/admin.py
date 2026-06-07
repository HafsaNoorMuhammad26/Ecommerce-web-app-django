from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'is_in_stock', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'get_item_count', 'get_total']
    inlines = [CartItemInline]
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Total Items'
    
    def get_total(self, obj):
        return f"${obj.get_total()}"
    get_total.short_description = 'Total Amount'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'created_at', 'total_amount', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'user__username', 'full_name']
    list_editable = ['status']
    inlines = [OrderItemInline]
    
    readonly_fields = ['order_id', 'created_at', 'total_amount']

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)