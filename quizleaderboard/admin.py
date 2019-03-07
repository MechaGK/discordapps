from django.contrib import admin

from quizleaderboard.models import User, Quiz, Entry

admin.site.register(User)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'date', 'creator')


admin.site.register(Entry)
