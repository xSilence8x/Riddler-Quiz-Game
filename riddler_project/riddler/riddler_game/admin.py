from django.contrib import admin

from .models import Question, QuizResult

admin.site.register(Question)
admin.site.register(QuizResult)