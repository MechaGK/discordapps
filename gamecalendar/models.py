from django.db import models


class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)
    cover = models.IntegerField()
    release_date = models.DateTimeField()
    hypes = models.IntegerField()
    name = models.CharField(max_length=64)
    updated_at = models.DateTimeField()
    url = models.URLField()


class FantasyCriticUser(models.Model):
    username = models.CharField(max_length=64)
    discord_username = models.CharField(max_length=64)


class FantasyCriticEntry(models.Model):
    game = models.OneToOneField(to=Game, on_delete=models.CASCADE)
    user = models.ManyToManyField(to=FantasyCriticUser)
