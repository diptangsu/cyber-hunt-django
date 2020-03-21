from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.team_name}'
