from django.db import models


class Question(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField()
    hint = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    points = models.IntegerField()
    visible = models.BooleanField()

    def __str__(self):
        return f'{self.name} [{self.points}]'


class Submission(models.Model):
    team = models.ForeignKey('teams.models.Team', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
