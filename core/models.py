from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File

class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.IntegerField(choices=[(i, f"Class {i}") for i in range(5, 13)])

    def __str__(self):
        return f"{self.name} (Class {self.class_level})"

class Flashcard(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter = models.CharField(max_length=200)
    question = models.TextField()
    answer = models.TextField()
    formula = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.chapter} - {self.question[:30]}"

class ExamDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()
    study_plan_generated = models.BooleanField(default=False)

class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=200)
    study_date = models.DateField()
    completed = models.BooleanField(default=False)

class Quiz(models.Model):
    chapter = models.CharField(max_length=200)
    questions = models.JSONField()   # [{"q": "...", "options": [...], "ans": 0}]

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Badge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='badges/')
    criteria = models.CharField(max_length=200)

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    badges_count = models.IntegerField(default=0)