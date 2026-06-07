from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('store:home')
    return wrapper