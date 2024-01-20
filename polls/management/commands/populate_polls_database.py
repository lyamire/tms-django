from django.core.management.base import BaseCommand
from polls.models import Question, Choice
from django.utils import timezone
import json


class Command(BaseCommand):
    help = 'Populates polls'

    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default='polls/management/commands/data.json')

    def handle(self, *args, **options):
        print('Remove all old questions and choices')
        Question.objects.all().delete()
        Choice.objects.all().delete()

        with open(options['data_file_path']) as data_file:
            data = json.load(data_file)
            for question_text, choices_dict in data.items():
                question = Question(question_text=question_text, pub_date=timezone.now())
                question.save()
                print(f'Question: {question}')
                for choice_text, votes in choices_dict.items():
                    choice = question.choices.create(choice_text=choice_text, votes=votes)
                    print(f'Choice: {choice}')
