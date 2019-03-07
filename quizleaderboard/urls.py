from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:quiz_pk>/', views.view_quiz, name='view-quiz'),
]
