# Generated by Django 5.0.3 on 2024-03-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riddler_game', '0002_quizresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizresult',
            name='date_taken',
            field=models.DateTimeField(),
        ),
    ]
