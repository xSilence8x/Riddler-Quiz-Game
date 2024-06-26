from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    """
    Every question in the quiz consists of question, right answer and hint.
    """
    question = models.TextField(max_length=250)
    answer = models.CharField(max_length=50)
    hint = models.CharField(max_length=50)


    def __str__(self):
        return self.question[:15]


class QuizResult(models.Model):
    """
    Every quiz that user takes saves data to database. 
    We collect username, date of quiz taken, percent and score, JS and Django elapsed time for comparison."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField()
    percent = models.IntegerField(default=0)
    score = models.IntegerField()
    time = models.IntegerField()
    django_time = models.FloatField(default=0)
    

    def __str__(self):
        return f"{self.user}, {self.percent} %, JS čas: {self.time} s, Django čas: {round(self.django_time)} s"