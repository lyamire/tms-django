from django import forms
from django.utils import timezone


class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=100)
    publication_date = forms.DateField(initial=timezone.now().date(), widget=forms.SelectDateWidget())
    choices = forms.CharField(label='Choices', widget=forms.Textarea)

