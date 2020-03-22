import os

from django.db.models.functions import Coalesce
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from CyberHuntDjango.decorators import login_required_custom
from teams.models import Team
from .models import Question
from .models import Submission


def get_question_images_and_files(question_id):
    base_path = f'./questions/static/questionsdata/{question_id}/'
    images_path = os.path.join(base_path, 'images')
    files_path = os.path.join(base_path, 'files')

    question_images = None
    question_files = None
    if os.path.exists(images_path):
        question_images = [
            os.path.join(f'questionsdata/{question_id}/images', image_name)
            for image_name in os.listdir(images_path)
        ]
    if os.path.exists(files_path):
        question_files = [
            os.path.join(f'questionsdata/{question_id}/files', filename)
            for filename in os.listdir(files_path)
        ]

    return question_images, question_files


def get_all_questions():
    all_questions = Question.objects.values('id', 'name', 'points')

    def inner():
        return all_questions

    return inner


get_all_questions = get_all_questions()


def get_team_score(team):
    team_submissions_points = Submission.objects.filter(team=team).aggregate(score=Coalesce(Sum('question__points'), 0))
    team_score = team_submissions_points['score']

    return team_score


@login_required_custom
def question(request, question_id):
    this_question = get_object_or_404(Question, id=question_id)
    question_images, question_files = get_question_images_and_files(question_id)
    all_questions = get_all_questions()

    team = Team.objects.get(id=request.session['team_id'])
    score = get_team_score(team)

    return render(request, 'questions/question.html', {
        'team': team,
        'score': score,
        'question': this_question,
        'files': question_files,
        'images': question_images,
        'questions_list': all_questions
    })


def submissions(request):
    all_submissions = Question.objects \
        .values('id', 'name') \
        .order_by('id') \
        .annotate(submissions=Count('submission'))

    return render(request, 'questions/submissions.html', {
        'submissions': all_submissions
    })


def leaderboard(request):
    team_scores = Team.objects \
        .values('team_name') \
        .order_by('team_name') \
        .annotate(score=Coalesce(Sum('submission__question__points'), 0)) \
        .order_by('-score')

    return render(request, 'questions/leaderboard.html', {
        'team_scores': team_scores,
    })
