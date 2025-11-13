from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .whatsapp import handle_whatsapp_webhook
from .ncert import ncert_url
import qrcode
from io import BytesIO
import json

def home(request):
    return render(request, 'dashboard.html')

@login_required
def flashcards_view(request, class_num, subject_name, chapter):
    subject = Subject.objects.get(name__iexact=subject_name, class_level=class_num)
    cards = Flashcard.objects.filter(subject=subject, chapter=chapter)
    return render(request, 'flashcards.html', {'cards': cards, 'chapter': chapter})

@login_required
def quiz_view(request, chapter):
    quiz = get_object_or_404(Quiz, chapter=chapter)
    if request.method == 'POST':
        score = 0
        for i, q in enumerate(quiz.questions):
            if request.POST.get(f'q{i}') == str(q['ans']):
                score += 1
        Score.objects.create(user=request.user, quiz=quiz, score=score)
        from .tasks import update_leaderboard
        update_leaderboard.delay(request.user.id)

        # badge
        if score == len(quiz.questions):
            badge, _ = Badge.objects.get_or_create(
                name="Chapter Master",
                defaults={'criteria': '100% in quiz', 'icon': 'badges/master.png'}
            )
            UserBadge.objects.get_or_create(user=request.user, badge=badge)

        return render(request, 'result.html', {
            'score': score,
            'total': len(quiz.questions),
            'chapter': chapter
        })
    return render(request, 'quiz.html', {'quiz': quiz, 'chapter': chapter})

@login_required
def qr_formula(request, class_num, subject_name, chapter):
    subject = Subject.objects.get(name__iexact=subject_name, class_level=class_num)
    formulas = Flashcard.objects.filter(
        subject=subject, chapter=chapter, formula__isnull=False
    ).values_list('formula', flat=True)
    data = "\n---\n".join(formulas)
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')

@login_required
def leaderboard(request):
    leaders = Leaderboard.objects.select_related('user').order_by('-total_score')[:50]
    return render(request, 'leaderboard.html', {'leaders': leaders})

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        return HttpResponse(handle_whatsapp_webhook(request), content_type='text/xml')
    return HttpResponse("OK")