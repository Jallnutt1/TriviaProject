from django.shortcuts import render, redirect
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
    question = getQuestion(request)
    context = context | question
    # context['question'] = Collection.objects.get(id=1).questions.get(id=request.session['counter'])
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
        test_collection = Collection.objects.get(id=1)
        new_question = Question.objects.create(copy=request.POST['question'],answer=request.POST['answer'],wrong1=request.POST['wrong1'],wrong2=request.POST['wrong2'],wrong3=request.POST['wrong3'],collection=test_collection)
        # new_question.collection.add(test_collection)
        return redirect('/addQuestion')
    else:
        context={
            'questions':Question.objects.all()
        }
        return render(request, "appTrivia/create.html",context)

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
    if request.session['addSecondPlayer'] == False:
        only_player = User.objects.get(id = request.session['first_player_id'])
        new_game = Game.objects.create(numberOfPlayers=1, whoseTurn=1, counter=1, player_1=only_player, player_1_score=0)
    else:
        first_player = User.objects.get(id = request.session['first_player_id'])
        second_player = User.objects.get(id = request.session['second_player_id'])
        new_game = Game.objects.create(numberOfPlayers=2, whoseTurn=1, counter=1, player_1=first_player, player_1_score=0, player_2=second_player, player_2_score=0)

    request.session['game_id'] = new_game.id 
    request.session['collection_id'] = 1
    return redirect('/qStage')

def getQuestion(request):
    counter = Game.objects.get(id=request.session['game_id']).counter
    question = Collection.objects.get(id=request.session['collection_id']).questions.get(id=counter)
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
        print('You got the right answer')
        if current_game.whoseTurn == 1:
            current_game.player_1_score = current_game.player_1_score + 10
            current_game.save()
            print(current_game.player_1_score)
        else:
            current_game.player_2_score = current_game.player_2_score + 10
            current_game.save()
            print(current_game.player_2_score)
    else:
        if current_game.whoseTurn == 1:
            current_game.player_1_score = current_game.player_1_score - 5
            current_game.save()
            print(current_game.player_1_score)
        else:
            current_game.player_2_score = current_game.player_2_score - 5
            current_game.save()
            print(current_game.player_2_score)

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

    if current_game.counter <= len(Collection.objects.get(id=request.session['collection_id']).questions.all()):
        return redirect('/qStage')
    else:
        return redirect('/winner')