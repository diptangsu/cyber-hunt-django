from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import Team
from CyberHuntDjango.decorators import check_login


def index(request):
    return redirect('login')


def register(request):
    if request.method == 'GET':
        return render(request, 'teams/register.html')
    else:
        team_name = request.POST.get('teamname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if all((team_name, phone, email, password, password2)):
            if password == password2:
                team = Team(team_name=team_name, phone=phone, email=email, password=password)
                team.save()

                messages.success(request, 'New team added successfully')
                return redirect('question', question_id=1)
            else:
                messages.error(request, 'Passwords don\'t match')
                return render(request, 'teams/register.html')
        else:
            messages.error(request, 'All fields are required')
            return render(request, 'teams/register.html')


def login(request):
    if 'team_id' in request.session:
        messages.info(request, 'You are already logged in')
        return redirect('question', question_id=1)
    if request.method == 'GET':
        return render(request, 'teams/login.html')
    else:
        email = request.POST.get('teamname')
        password = request.POST.get('password')

        if email and password:
            try:
                team = Team.objects.get(email=email, password=password)
                request.session['team_id'] = team.id

                return redirect('question', question_id=1)
            except Team.DoesNotExist:
                messages.error(request, 'Team name or password incorrect')
                return render(request, 'teams/login.html')
        else:
            messages.error(request, 'Team name or password fields are required')
            return render(request, 'teams/login.html')


@check_login
def logout(request):
    del request.session['team_id']
    return redirect('login')
