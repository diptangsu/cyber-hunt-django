import os

from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from CyberHuntDjango.decorators import login_required_custom
from teams.models import Team
from .models import Question
from .models import Submission


def get_question_images_files_and_links(question_id):
    base_path = f'./questions/static/questionsdata/{question_id}/'
    images_path = os.path.join(base_path, 'images')
    files_path = os.path.join(base_path, 'files')
    links_path = os.path.join(base_path, 'links')

    question_images = None
    question_files = None
    question_links = None
    if os.path.exists(images_path):
        question_images = [
            {
                'path': os.path.join(f'questionsdata/{question_id}/images', image_name),
                'name': image_name
            }
            for image_name in os.listdir(images_path)
        ]
    if os.path.exists(files_path):
        question_files = [
            {
                'path': os.path.join(f'questionsdata/{question_id}/files', filename),
                'name': filename
            }
            for filename in os.listdir(files_path)
        ]
    if os.path.exists(links_path):
        question_links = [
            {
                'path': os.path.join(f'questionsdata/{question_id}/links', link_name),
                'name': link_name
            }
            for link_name in os.listdir(links_path)
            if link_name.endswith('.html')
        ]

    return question_images, question_files, question_links


def get_all_questions():
    all_questions = Question.objects.values('id', 'name', 'points').filter(visible=True)

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
    question_images, question_files, question_links = get_question_images_files_and_links(question_id)
    all_questions = get_all_questions()

    team = Team.objects.get(id=request.session['team_id'])
    score = get_team_score(team)

    questions_answered = set(
        Submission.objects.values_list('question__id', flat=True).filter(team=team)
    )

    return render(request, 'questions/question.html', {
        'team': team,
        'score': score,
        'question': this_question,
        'questions_answered': questions_answered,
        'files': question_files,
        'images': question_images,
        'links': question_links,
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
