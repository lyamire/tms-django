import os

def populate_polls_database(source: str, clean_database: bool = False):
    import json
    from polls.models import Choice, Question
    from django.utils import timezone

    with open(source, 'r') as data_file:
        data = json.load(data_file)

    if clean_database:
        Choice.objects.all().delete()
        Question.objects.all().delete()

    for item in data:
        question = Question.objects.create(question_text=item, pub_date=timezone.now())

        for text, votes in data[item].items():
            choice = question.choices.create(choice_text=text, votes=votes)

        question.save()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    import django
    django.setup()

    populate_polls_database('data.json')
