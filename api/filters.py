from django.db.models import QuerySet, Count
from django.db.models.functions import Length
from rest_framework import filters
from rest_framework.request import Request

class ChoiceCountFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        min_choice_count = request.query_params.get('min_choice_count')
        max_choice_count = request.query_params.get('max_choice_count')
        if min_choice_count is not None:
            queryset = queryset.annotate(choice_count=Count('choices')).filter(choice_count__gte=min_choice_count)
        if max_choice_count is not None:
            queryset = queryset.annotate(choice_count=Count('choices')).filter(choice_count__lte=max_choice_count)
        return queryset

class ArticleMinTextLengthFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        min_article_text_length = request.query_params.get('min_article_text_length')
        if min_article_text_length is not None:
            queryset = queryset.annotate(text_length=Length('text')).filter(text_length__gte=min_article_text_length)
        return queryset
