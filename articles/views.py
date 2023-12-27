from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import ArticleForm
from .models import Article
# Create your views here.

def index(request):
    context = {
        'articles': Article.objects.filter(status=Article.Status.APPROVED)
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, status=Article.Status.APPROVED)
    return render(request, 'articles/detail.html', {'article': article})

def like(request, article_id):
    article = get_object_or_404(Article, id=article_id, status=Article.Status.APPROVED)
    article.like_count += 1
    article.save()
    return redirect('articles:detail', article_id=article_id)

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            author = form.cleaned_data['author']
            article = Article(title=title, text=text, author=author)
            article.save()
            messages.success(
                request, 'Your article is added and will be '
                         'displayed once reviewed by administrator')
            return redirect('articles:index')
    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form})
