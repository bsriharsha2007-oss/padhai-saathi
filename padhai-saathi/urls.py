from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'flashcards/<int:class_num>/<str:subject_name>/<str:chapter>/',
        views.flashcards_view,
        name='flashcards'
    ),

    path(
        'quiz/<str:chapter>/',
        views.quiz_view,
        name='quiz'
    ),

    path(
        'result/',
        views.result_redirect,
        name='result'
    ),

    path(
        'qr/<int:class_num>/<str:subject_name>/<str:chapter>/',
        views.qr_formula,
        name='qr_formula'
    ),

    path(
        'leaderboard/',
        views.leaderboard,
        name='leaderboard'
    ),

    path(
        'whatsapp/webhook/',
        views.whatsapp_webhook,
        name='whatsapp_webhook'
    ),
]
