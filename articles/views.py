from django.shortcuts import render, get_object_or_404
from .models import Article
# Create your views here.

def index(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/detail.html', {'article': article})
