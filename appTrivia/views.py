from django.shortcuts import render, redirect
from django.contrib import messages
from LoginReg.models import *
from .models import *
import random


def index(request):
    request.session['addSecondPlayer'] = False
    return render(request, "appTrivia/index.html")

def gameStage(request):
    if request.session['addSecondPlayer'] == False:
        request.session['first_player_id'] = request.session['user_id']
    else:
        request.session['second_player_id'] = request.session['user_id']
    context = oneOrTwoPlayers(request)
    collection_dict = {'all_collections':Collection.objects.all()}
    context.update(collection_dict)
    return render(request, "appTrivia/gameStage.html", context)

def addSecondPlayer(request):
    request.session['addSecondPlayer'] = True
    return redirect ('/access/playerLogin')

def qStage(request):
    context = oneOrTwoPlayers(request)
    context['whosTurn'] = Game.objects.get(id=request.session['game_id']).whoseTurn
    return render(request, "appTrivia/qStage.html", context)

def question(request):
    context = oneOrTwoPlayers(request)
    question_1 = getQuestion(request)
    context.update(question_1)
    return render(request, "appTrivia/question.html", context)

def leaderboard(request):
    context = {
        'all_games':Game.objects.all()
    }
    return render(request, "appTrivia/leaderboard.html", context)

def winner(request):
    context = {
        'game': Game.objects.get(id = request.session['game_id'])
    }
    return render(request, "appTrivia/winner.html",context)

def addQuestion(request):
    if request.method == "POST":
        errors = Question.objects.question_regulator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addQuestion')
        else:
            collection = Collection.objects.get(id=request.POST['collection_id'])
            Question.objects.create(copy=request.POST['question'],answer=request.POST['answer'],wrong1=request.POST['wrong1'],wrong2=request.POST['wrong2'],wrong3=request.POST['wrong3'],collection=collection)
            return redirect('/addQuestion')
    else:
        context={
            'questions':Question.objects.all(),
            'collections':Collection.objects.all()
        }
        return render(request, "appTrivia/create.html",context)

def addCollection(request):
    if request.method == "POST":
        errors = Collection.objects.collection_regulator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addQuestion')
        else:
            Collection.objects.create(collection_name=request.POST['new_collection'])
            return redirect ('/addQuestion')

def oneOrTwoPlayers(request):
    if request.session['addSecondPlayer'] == False:
        context={
            'user1':User.objects.get(id=request.session['first_player_id']),
        }
    else:
        context={
            'user1':User.objects.get(id=request.session['first_player_id']),
            'user2':User.objects.get(id=request.session['second_player_id'])
        }
    return context

def newGame(request):
    if request.method == 'POST':
        if request.session['addSecondPlayer'] == False:
            only_player = User.objects.get(id = request.session['first_player_id'])
            new_game = Game.objects.create(numberOfPlayers=1, whoseTurn=1, counter=0, player_1=only_player, player_1_score=0)
        else:
            first_player = User.objects.get(id = request.session['first_player_id'])
            second_player = User.objects.get(id = request.session['second_player_id'])
            new_game = Game.objects.create(numberOfPlayers=2, whoseTurn=1, counter=0, player_1=first_player, player_1_score=0, player_2=second_player, player_2_score=0)

        request.session['game_id'] = new_game.id 
        request.session['collection_id'] = request.POST['collection_id']
        return redirect('/qStage')

def getQuestion(request):
    counter = Game.objects.get(id=request.session['game_id']).counter
    question = Collection.objects.get(id=request.session['collection_id']).questions.all()[counter]
    request.session['answer'] = question.answer
    option_list = [question.answer,question.wrong1,question.wrong2,question.wrong3]
    random.shuffle(option_list)
    questionDict = {
        'copy':question.copy,
    }
    for i in range (1,5):
        string = f'option{i}'
        questionDict[string] = option_list[i-1]
    return questionDict

def checkAnswer(request, selection):
    current_game = Game.objects.get(id=request.session['game_id'])
    if selection == request.session['answer']:
        if current_game.whoseTurn == 1:
            current_game.player_1_score = current_game.player_1_score + 10
            current_game.save()
        else:
            current_game.player_2_score = current_game.player_2_score + 10
            current_game.save()
    else:
        if current_game.whoseTurn == 1:
            current_game.player_1_score = current_game.player_1_score - 5
            current_game.save()
        else:
            current_game.player_2_score = current_game.player_2_score - 5
            current_game.save()

    if request.session['addSecondPlayer'] == True:
        if current_game.whoseTurn == 1:
            current_game.whoseTurn = 2
            current_game.save()

        else:
            current_game.whoseTurn = 1
            current_game.save()
            current_game.counter = current_game.counter + 1
            current_game.save()
    else:
        current_game.counter = current_game.counter + 1
        current_game.save()

    if current_game.counter < len(Collection.objects.get(id=request.session['collection_id']).questions.all()):
        return redirect('/qStage')
    else:
        return redirect('/winner')

def quitGame(request):
    game_to_delete = Game.objects.get(id=request.session['game_id'])
    game_to_delete.delete()
    return redirect('/access/logout')