from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    return redirect('login')


def register(request):
    ...


def login(request):
    return render(request, 'teams/login.html')


def logout(request):
    pass
