from django.contrib import admin
from .models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'authors', 'like_count', 'is_popular']}),
        ('Date information', {'fields': ['text']})
    ]
    readonly_fields = ['like_count', 'is_popular']
    search_fields = ['title', 'authors', 'text']
    list_display = ['title', 'is_popular']


admin.site.register(Article, ArticleAdmin)
