from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import RegistrationForm, CheckoutForm
from .decorators import admin_required

# Authentication Views
def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to HafsaCart, {username}!')
            return redirect('store:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'store:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:home')

# Product Views
def home(request):
    products = Product.objects.filter(stock__gt=0)
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        products = products.filter(category__icontains=category_filter)
    
    # Get unique categories for filter
    categories = sorted(set([c.strip().title() for c in Product.objects.values_list('category', flat=True) if c and c.strip()]))
    context = {
        'products': products,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Cart Views
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock <= 0:
        messages.error(request, 'This product is out of stock!')
        return redirect('store:product_detail', product_id=product_id)
    
    # Get or create cart for user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        # Check if increasing quantity would exceed stock
        if cart_item.quantity + 1 <= product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Added another {product.name} to your cart.')
        else:
            messages.error(request, f'Cannot add more {product.name}. Only {product.stock} in stock.')
    else:
        messages.success(request, f'{product.name} added to your cart!')
    
    return redirect('store:cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    if request.method == 'POST':
        # Update quantities
        for item in cart_items:
            quantity_key = f'quantity_{item.id}'
            remove_key = f'remove_{item.id}'
            
            if quantity_key in request.POST:
                new_quantity = int(request.POST[quantity_key])
                if new_quantity > 0:
                    if new_quantity <= item.product.stock:
                        item.quantity = new_quantity
                        item.save()
                    else:
                        messages.error(request, f'Only {item.product.stock} units of {item.product.name} available.')
                else:
                    item.delete()
            
            elif remove_key in request.POST:
                item.delete()
                messages.info(request, f'{item.product.name} removed from cart.')
        
        return redirect('store:cart')
    
    total = cart.get_total()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f'{product_name} removed from your cart.')
    return redirect('store:cart')

# Order Views
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:home')
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'{item.product.name} only has {item.product.stock} units in stock. Please adjust your quantity.')
            return redirect('store:cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total(),
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
            )
            
            # Create order items and update stock
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                )
                # Reduce stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # Clear cart
            cart.clear_cart()
            
            messages.success(request, f'Order placed successfully! Your order ID is {order.order_id}. Thank you for shopping at HafsaCart.')
            return redirect('store:order_success', order_id=order.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form with user data
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': cart.get_total(),
        'form': form,
    }
    return render(request, 'store/checkout.html', context)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

# Admin Views
@login_required
@admin_required
def admin_dashboard(request):
    from django.db.models import Sum
    
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(stock__lt=10).count()
    
    # Fixed revenue calculation
    delivered_orders = Order.objects.filter(status='Delivered')
    total_revenue = delivered_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    recent_orders = Order.objects.all()[:10]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'low_stock': low_stock,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'store/admin/admin_dashboard.html', context)
@login_required
@admin_required
def admin_orders(request):
    orders = Order.objects.all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'store/admin/admin_orders.html', {'orders': orders, 'status_filter': status_filter})

@login_required
@admin_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order {order.order_id} status updated to {new_status}')
            return redirect('store:admin_order_detail', order_id=order.id)
    
    return render(request, 'store/admin/admin_order_detail.html', {'order': order})