from django.db import models
from core_app.models import UserAccount


# Quiz Model (A quiz is a collection of questions)
class Quiz(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Quizzes"

# MCQ Model
class Question(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    correct_choice = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) # CASCADE means all questions will be deleted if their quiz is deleted


    def __str__(self):
        return self.question_text

    @property
    def get_choices(self):
        return [self.choice1, self.choice2, self.choice3, self.choice4]

# True/False Model
class TrueFalse(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    is_true = models.BooleanField(default=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "TrueFalse-Questions"

    def __str__(self):
        return self.question_text

    @property
    def get_choices(self):
        return ['True', 'False']

class UserQuizScore(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE)
    score = models.IntegerField()
    #date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name} - {self.score}"
