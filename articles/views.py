from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
# Create your views here.

def articles(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request, 'articles.html', context)
