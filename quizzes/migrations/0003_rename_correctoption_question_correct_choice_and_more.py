# Generated by Django 5.1.6 on 2025-02-24 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_truefalse_quiz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='correctOption',
            new_name='correct_choice',
        ),
        migrations.RenameField(
            model_name='truefalse',
            old_name='isTrue',
            new_name='is_true',
        ),
    ]
