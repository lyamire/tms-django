from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', widget=forms.Textarea)
    author = forms.CharField(label='Author', max_length=100)
