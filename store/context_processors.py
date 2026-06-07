from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.get_item_count()
    else:
        cart_count = 0
    
    return {
        'cart_count': cart_count,
        'cart_total': getattr(cart, 'get_total', lambda: 0)() if request.user.is_authenticated else 0,
    }