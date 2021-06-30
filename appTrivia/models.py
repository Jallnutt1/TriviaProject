from django.db import models

class Collection(models.Model):
    collection_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Question(models.Model):
    copy=models.CharField(max_length=255)
    answer=models.CharField(max_length=255)
    wrong1=models.CharField(max_length=255)
    wrong2=models.CharField(max_length=255)
    wrong3=models.CharField(max_length=255)
    collection=models.ForeignKey(Collection, related_name="questions", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Game(models.Model):
    numberOfPlayers=models.IntegerField()
    whoseTurn=models.IntegerField()
    counter = models.IntegerField()
    player_1 = models.ForeignKey('LoginReg.User', related_name='game_p1', on_delete=models.CASCADE)
    player_1_score = models.IntegerField()
    player_2 = models.ForeignKey('LoginReg.User', related_name='game_p2', blank=True, null=True, on_delete=models.CASCADE)
    player_2_score = models.IntegerField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)