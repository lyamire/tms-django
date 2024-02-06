from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.request import Request

from articles.models import Article, Author
from polls.models import Question, Choice
from shop.models import Category, Product
from .serializers import (QuestionSerializer, ChoiceSerializer,
                          ArticleSerializer, AuthorSerializer,
                          ProductSerializer, CategorySerializer)
from .filters import ChoiceCountFilter, ArticleMinTextLengthFilter

#polls
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().prefetch_related('choices')
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
    question = get_object_or_404(Question, id=question_id, status=Question.Status.APPROVED,
                                 pub_date__lte=timezone.now())
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)

#articles
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ArticleMinTextLengthFilter]
    ordering_fields = ['id', 'title', 'like_count']
    search_fields = ['id','title', 'text', 'like_count', 'status']

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

