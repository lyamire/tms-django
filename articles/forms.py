from django import forms

from articles.models import Author


class ArticleForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', widget=forms.Textarea)
    authors = forms.ModelMultipleChoiceField(label='Authors',
                                             queryset=Author.objects.all())
