from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
