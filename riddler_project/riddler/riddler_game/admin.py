from django.contrib import admin
from .models import Question, QuizResult
from django.utils import timezone


class QuizResultAdmin(admin.ModelAdmin):
    list_display = ["get_quiz_result", 'date_taken_display']


    def get_quiz_result(self, obj):
        return str(obj)
    

    def date_taken_display(self, obj):
        return timezone.localtime(obj.date_taken).strftime('%Y-%m-%d %H:%M:%S')

    get_quiz_result.short_description = "Výsledky kvízu"
    date_taken_display.short_description = "Datum kvízu"

admin.site.register(Question)
admin.site.register(QuizResult, QuizResultAdmin)