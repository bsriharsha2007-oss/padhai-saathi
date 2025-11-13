from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import ExamDate, StudyPlan, Flashcard, Leaderboard

@shared_task
def generate_study_plan(user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    exams = ExamDate.objects.filter(user=user, study_plan_generated=False)
    for exam in exams:
        days_left = (exam.exam_date - timezone.now().date()).days
        if days_left <= 0:
            continue
        chapters = Flashcard.objects.filter(
            subject__name__icontains=exam.subject,
            subject__class_level__lte=12
        ).values_list('chapter', flat=True).distinct()
        chapters = list(set(chapters))
        per_day = max(1, len(chapters) // max(1, days_left - 2))
        for i, ch in enumerate(chapters):
            study_date = timezone.now().date() + timedelta(days=i // per_day)
            StudyPlan.objects.create(
                user=user,
                subject=exam.subject,
                chapter=ch,
                study_date=study_date
            )
        exam.study_plan_generated = True
        exam.save()
    update_leaderboard.delay(user_id)

@shared_task
def update_leaderboard(user_id):
    user = User.objects.get(id=user_id)
    lb, _ = Leaderboard.objects.get_or_create(user=user)
    lb.total_score = Score.objects.filter(user=user).aggregate(s=models.Sum('score'))['s'] or 0
    lb.badges_count = UserBadge.objects.filter(user=user).count()
    lb.save()