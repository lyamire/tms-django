from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import ArticleForm
from .models import Article, Author


# Create your views here.

def index(request):
    context = {
        'articles': Article.objects.filter(status=Article.Status.APPROVED)
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_id):
    article: Article = get_object_or_404(Article, id=article_id, status=Article.Status.APPROVED)

    authors = article.authors.all()
    return render(request, 'articles/detail.html', {'article': article, 'authors': authors})

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

            article = Article(title=title, text=text)
            article.save()

            authors_raw = form.cleaned_data['authors']
            article.authors.set(authors_raw)
            article.save()

            messages.success(
                request, 'Your article is added and will be '
                         'displayed once reviewed by administrator')
            return redirect('articles:index')
    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'articles/author_detail.html', {'author': author, 'articles': author.articles.all()})

def authors_list(request):
    authors = Author.objects.all()
    return render(request,'articles/authors_list.html', {'authors': authors})
