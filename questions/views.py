from django.shortcuts import render
from django.shortcuts import get_object_or_404
from CyberHuntDjango.decorators import check_login
import os

from .models import Question
from .models import Submission


@check_login
def question(request, question_id):
    print('ekhane', request.session.get('team_id', 'nei'))
    this_question = get_object_or_404(Question, id=question_id)
    question_files = 1
    question_images = 1

    all_questions = Question.objects.values_list('pk', 'name', 'points')

    return render(request, 'questions/question.html', {
        'question': this_question,
        'files': question_files,
        'images': question_images,
        'questions_list': all_questions
    })


def submissions(request):
    all_submissions = Submission.objects.all()
    return render(request, 'questions/submissions.html', {
        'submissions': all_submissions
    })


def leaderboard(request):
    ...
