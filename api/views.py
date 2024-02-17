from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.request import Request

from articles.models import Article, Author
from polls.models import Question, Choice
from shop.models import Category, Product
from .serializers import (QuestionSerializer, ChoiceSerializer,
                          ArticleSerializer, AuthorSerializer,
                          ProductSerializer, CategorySerializer)
from .filters import ChoiceCountFilter, ArticleMinTextLengthFilter

from rest_framework.decorators import api_view
from django.contrib.auth import login


#polls
def get_active_questions():
    return Question.objects \
        .annotate(choice_count=Count('choices')) \
        .filter(status=Question.Status.APPROVED,
                pub_date__lte=timezone.now(),
                choice_count__gte=2)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = get_active_questions().prefetch_related('choices')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ChoiceCountFilter]
    ordering_fields = ['id', 'question_text', 'pub_date']
    search_fields = ['id', 'question_text', 'pub_date']


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['choice_text', 'votes']
    search_fields = ['choice_text', 'question__question_text']

@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(get_active_questions(), id=question_id)
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)

@api_view(['POST'])
def register(request):
    if User.objects.filter(email=request.data['email']).exists():
        raise Exception('User already exists')

    if request.data['password'] != request.data['password2']:
        raise Exception('Passwords do not match')

    user = User.objects.create_user(
        request.data['username'],
        request.data['email'],
        request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )
    user.save()
    login(request, user)
    return HttpResponse(status=201)


#articles
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ArticleMinTextLengthFilter]
    ordering_fields = ['id', 'title', 'like_count']
    search_fields = ['id', 'title', 'text', 'like_count', 'status']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related('articles')
    serializer_class = AuthorSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'first_name', 'last_name', 'date_of_birth']
    search_fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'articles__title', 'articles__text']

#shop
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'name', 'price', 'category']
    search_fields = ['id', 'name', 'description', 'price', 'category',]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('products')
    serializer_class = CategorySerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']

