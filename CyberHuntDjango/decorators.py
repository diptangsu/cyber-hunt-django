from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def check_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'team_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, 'Please login to visit this page')
            return redirect('login')

    return wrapper
