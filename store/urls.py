from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Product URLs
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]