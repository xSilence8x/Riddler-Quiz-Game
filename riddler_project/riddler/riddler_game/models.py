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
    date_taken = models.DateTimeField(auto_now_add=False)
    score = models.IntegerField()
    time = models.IntegerField()
    

    def __str__(self):
        return f"{self.user}, skóre {self.score}, {self.time} s, {self.date_taken}"