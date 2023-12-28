from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Article(models.Model):
    class Status(models.TextChoices):
        NEW = 'NW', _('New')
        REJECTED = 'RJ', _('Rejected')
        APPROVED = 'AP', _('Approved')

    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.NEW)

    @admin.display(
        boolean=True,
        description='is popular'
        # ordering='like_count'
    )
    def is_popular(self):
        return self.like_count > 100

    def __str__(self):
        return self.title
