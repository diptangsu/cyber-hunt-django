from django.urls import path
from .views import *

urlpatterns = [
    path('question/<int:question_id>/', question, name='question'),
    path('submissions/', submissions, name='submissions'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]
