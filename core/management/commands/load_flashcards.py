from django.core.management.base import BaseCommand
import json
from core.models import Subject, Flashcard

class Command(Base20):
    def handle(self, *args, **options):
        with open('flashcards.json') as f:
            data = json.load(f)
        for item in data:
            subj, _ = Subject.objects.get_or_create(
                name=item['subject'],
                class_level=item['class']
            )
            Flashcard.objects.get_or_create(
                subject=subj,
                chapter=item['chapter'],
                question=item['question'],
                answer=item['answer'],
                formula=item.get('formula')
            )
        self.stdout.write("Flashcards loaded")