from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE)
    points = models.IntegerField()
