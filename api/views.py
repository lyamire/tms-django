from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import permissions, viewsets, filters, views
from rest_framework import status, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from articles.models import Article, Author
from polls.models import Question, Choice
from shop.models import Category, Order, OrderEntry, Product, Profile, StatusOrder
from .serializers import (CurrentUserSerializer, QuestionSerializer, ChoiceSerializer,
                          ArticleSerializer, AuthorSerializer,
                          ProductSerializer, CategorySerializer, OrderSerializer, RegistrationSerializer,
                          UpdateOrderSerializer)
from .filters import CategoryIDFilter, ChoiceCountFilter, ArticleMinTextLengthFilter

from rest_framework.decorators import api_view
from django.contrib.auth import login


#polls
def get_active_questions():
    return Question.objects \
        .annotate(choice_count=Count('choices')) \
        .filter(status=Question.Status.APPROVED,
                # pub_date__lte=timezone.now(),
                # choice_count__gte=2
                )

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

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

# articles
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
class ProductViewSet(viewsets.mixins.RetrieveModelMixin,
                     viewsets.mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, CategoryIDFilter]
    # ordering_fields = ['id', 'name', 'price', 'category']
    # search_fields = ['id', 'name', 'description', 'price', 'category',]

class CategoryViewSet(viewsets.mixins.RetrieveModelMixin,
                      viewsets.mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all().prefetch_related('products').order_by('-id')
    serializer_class = CategorySerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    # ordering_fields = ['id', 'name']
    # search_fields = ['id', 'name']

class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        active_order = Profile.init_shopping_cart(request.user)

        entry = OrderEntry.objects.get_or_create(order=active_order, product=product)[0]

        entry.count += 1
        entry.save()

        return Response(status=status.HTTP_200_OK)

class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(OrderSerializer(request.user.profile.shopping_cart).data)

class UpdateCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request):
        update_order = UpdateOrderSerializer(data=request.data)
        update_order.is_valid(raise_exception=True)

        order: Order = request.user.profile.shopping_cart
        update_order_data: dict = update_order.validated_data
        self._update_order(order, update_order_data)
        return Response(OrderSerializer(order).data)

    def _update_order(self, order: Order, update_order_data: dict):
        if update_order_data['clear']:
            order.order_entries.all().delete()
        else:
            for update_order_entry_data in update_order_data['order_entries']:
                self._update_order_entry(order, update_order_entry_data)

    def _update_order_entry(self, order: Order, update_order_entry_data: dict):
        order_entry_id = update_order_entry_data['id']
        order_entry = order.order_entries.filter(id=order_entry_id).first()
        if order_entry is None:
            raise ValidationError(f'Unknown order entry id {order_entry_id}')
        if update_order_entry_data['remove']:
            order_entry.delete()
        elif update_order_entry_data['count'] is not None:
            order_entry.count = update_order_entry_data['count']
            order_entry.save()

class CompleteOrderView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile: Profile = Profile.objects.filter(user=request.user).first()

        order = profile.shopping_cart
        order.status = StatusOrder.COMPLETED
        order.save()

        profile.shopping_cart = None
        profile.save()
        return Response(status=status.HTTP_200_OK)

class CurrentUserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user

class OrdersViewSet(viewsets.ModelViewSet,
                    viewsets.mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class RepeatOrderView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        order_id = request.data.get('order_id')
        order_old: Order = Order.objects.filter(id=order_id).first()
        old_entries = []
        for entry in order_old.order_entries.all().order_by('id'):
            old_entries.append(entry)

        active_order = Profile.init_shopping_cart(request.user)

        for old_entry in old_entries:
            entry = OrderEntry.objects.get_or_create(order=active_order, product=old_entry.product)[0]

            entry.count = old_entry.count
            entry.save()
        return Response(status=status.HTTP_200_OK)