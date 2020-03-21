from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    return redirect('login')


def register(request):
    if request.method == 'GET':
        return render(request, 'teams/register.html')
    else:
        pass


def login(request):
    if request.method == 'GET':
        return render(request, 'teams/login.html')
    else:
        pass


def logout(request):
    pass
