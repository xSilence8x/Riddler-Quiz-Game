from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question = models.TextField(max_length=250)
    answer = models.CharField(max_length=50)
    hint = models.CharField(max_length=50)


    def __str__(self):
        return self.question[:15]


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField()
    percent = models.IntegerField(default=0)
    score = models.IntegerField()
    time = models.IntegerField()
    django_time = models.FloatField(default=0)
    

    def __str__(self):
        return f"{self.user}, {self.percent} %, JS čas: {self.time} s, Django čas: {self.django_time}"