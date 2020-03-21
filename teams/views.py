from django.shortcuts import render


def register(request):
    return render(request, 'teams/index.html')


def login(request):
    pass


def logout(request):
    pass
