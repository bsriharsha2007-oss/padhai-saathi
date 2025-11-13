import re
from datetime import datetime
from django.contrib.auth.models import User
from .models import ExamDate
from .tasks import generate_study_plan

def parse_exam_message(text):
    pattern = r"(\w+).*?(\d{1,2}[\/-]\d{1,2}[\/-]\d{2,4})"
    matches = re.finditer(pattern, text, re.IGNORECASE)
    exams = []
    for m in matches:
        subject = m.group(1).capitalize()
        date_str = m.group(2).replace('-', '/')
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y").date()
        except:
            try:
                dt = datetime.strptime(date_str, "%d/%m/%y").date()
            except:
                continue
        exams.append({"subject": subject, "date": dt})
    return exams

def handle_whatsapp_webhook(request):
    from twilio.twiml.messaging_response import MessagingResponse
    message = request.POST.get('Body', '')
    from_number = request.POST.get('From').replace('whatsapp:', '')

    # Find user by phone (you must store phone in a Profile model)
    try:
        user = User.objects.get(profile__phone=from_number)
    except:
        resp = MessagingResponse()
        resp.message("Sorry, we couldn't identify you.")
        return str(resp)

    exams = parse_exam_message(message)
    for e in exams:
        ExamDate.objects.create(user=user, subject=e['subject'], exam_date=e['date'])
    generate_study_plan.delay(user.id)

    resp = MessagingResponse()
    resp.message(f"Found {len(exams)} exam(s). Study plan generating...")
    return str(resp)