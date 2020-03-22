from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def login_required_custom(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'team_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, 'Please login to visit this page', 'danger')
            return redirect('login')

    return wrapper
