from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.TextField(max_length=250)
    answer = models.CharField(max_length=50)
    hint = models.CharField(max_length=50)


    def __str__(self):
        return self.question[:15]


