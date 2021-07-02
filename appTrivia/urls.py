from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('gameStage',views.gameStage),
    path('addSecondPlayer',views.addSecondPlayer),
    path('qStage',views.qStage),
    path('question',views.question),
    path('leaderboard',views.leaderboard),
    path('winner',views.winner),
    path('addQuestion',views.addQuestion),
    path('addCollection',views.addCollection),
    path('newGame',views.newGame),
    path('checkAnswer/<str:selection>',views.checkAnswer),
    path('quitGame',views.quitGame)
    # path('guestPlayer',views.guestPlayer)
]