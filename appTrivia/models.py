from django.db import models

class CollectionManager(models.Manager):
    def collection_regulator(self, postData):
        errors = {}
        if not postData['new_collection']:
            errors['new_collection'] = "Please enter a name for your new collection"
        return errors

class Collection(models.Model):
    collection_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=CollectionManager()

class QuestionManager(models.Manager):
    def question_regulator(self, postData):
        errors = {}
        if not postData['question']:
            errors['question'] = "Please fill in QUESTION field"
        if not postData['answer']:
            errors['answer'] = "Please fill in ANSWER field"
        if not postData['wrong1']:
            errors['wrong1'] = "Please fill in FIRST WRONG ANSWER field"
        if not postData['wrong2']:
            errors['wrong2'] = "Please fill in SECOND WRONG ANSWER field"
        if not postData['wrong3']:
            errors['wrong3'] = "Please fill in THIRD WRONG ANSWER field"
        return errors

class Question(models.Model):
    copy=models.CharField(max_length=255)
    answer=models.CharField(max_length=255)
    wrong1=models.CharField(max_length=255)
    wrong2=models.CharField(max_length=255)
    wrong3=models.CharField(max_length=255)
    collection=models.ForeignKey(Collection, related_name="questions", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=QuestionManager()

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