from django.db.models import signals
from django.dispatch import receiver

from polls.models import Question, Choice


@receiver(signals.post_save, sender=Question)
def save_question(instance: Question, **kwargs):
    print(f'Saved question: {instance.id}. Status: "{instance.status}", Text: "{instance.question_text}"')

@receiver(signals.post_delete, sender=Question)
def delete_question(instance: Question, **kwargs):
    print(f'Deleted question: {instance.id}')

@receiver(signals.post_save, sender=Choice)
def save_choice(instance: Choice, **kwargs):
    print(f'Saved choice: {instance.id} for Question: {instance.question_id}. {instance.choice_text}')

@receiver(signals.post_delete, sender=Choice)
def delete_choice(instance: Choice, **kwargs):
    print(f'Deleted choice: {instance.id} from Question: {instance.question_id}')