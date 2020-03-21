from django.urls import path
from .views import *

urlpatterns = [
    path('question/<int:question_id>/', question),
    path('submissions/', submissions),
    path('leaderboard/', leaderboard),
]
