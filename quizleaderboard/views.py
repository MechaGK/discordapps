from django.shortcuts import render, get_object_or_404

from quizleaderboard.models import Quiz, Entry


def index(request):
    quiz_list = Quiz.objects.order_by('-date').all()
    return render(request, 'quizleaderboard/index.html', context={'quiz_list': quiz_list})


def view_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    entries = Entry.objects.filter(quiz=quiz).order_by('-points')
    return render(request, 'quizleaderboard/view.html', context={'quiz': quiz, 'entries': entries})
