from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('playerLogin',views.playerLogin),
    path('register',views.register),
    path('editRegister',views.editRegister),
    path('login',views.login),
    path('editLogin',views.editLogin),
    path('logout',views.logout),
    path('show_all',views.show_all),
    path('delete/<int:user_id>',views.delete),
    path('update',views.update),
    path('change_password',views.change_password),
    path('playAsGuest', views.playAsGuest)
]
