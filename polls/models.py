from datetime import datetime, UTC

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import signals


# Create your models here.
class Question(models.Model):
    class Status(models.TextChoices):
        NEW = 'NW', _('New')
        REJECTED = 'RJ', _('Rejected')
        APPROVED = 'AP', _('Approved')

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Date published', default=datetime.now(UTC), db_index=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.NEW)

    @admin.display(
        boolean=True,
        description='Published recently?',
        ordering='pub_date'
    )
    def was_published_recently(self):
        now = datetime.now(UTC)
        return (now - timezone.timedelta(days=1)) <= self.pub_date <= now

    def __str__(self):
        return self.question_text

@receiver(signals.post_save, sender=Question)
def create_question(instance, **kwargs):
    print(f'Saved question: {instance.id}. Status: {instance.status}')

@receiver(signals.post_init, sender=Question)
def init_question(instance, **kwargs):
    print(f'Created question: {instance.id}. Question: {instance.question_text}')

@receiver(signals.post_delete, sender=Question)
def delete_question(instance, **kwargs):
    print(f'Deleted question: {instance.id}')


class Choice(models.Model):
    question: Question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    @admin.display(ordering='question__question_text', description='Question Text')
    def get_question_text(self):
        return self.question.question_text

    def __str__(self):
        return f'{self.question.question_text} - {self.choice_text}'
