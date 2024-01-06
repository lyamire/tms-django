from django.contrib import admin
from .models import Article, Author


# Register your models here.

# class AuthorInLine(admin.TabularInline):
#     model = Author
#     extra = 1

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'like_count', 'is_popular']}),
        ('Date information', {'fields': ['text']})
    ]
    readonly_fields = ['like_count', 'is_popular']
    search_fields = ['title', 'text']
    list_display = ['title', 'is_popular']
    # inlines = [AuthorInLine]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
