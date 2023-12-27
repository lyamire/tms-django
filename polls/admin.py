from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ['votes']
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['was_published_recently']
    fieldsets = [
        (None, {'fields': ['question_text', 'status']}),
        ('Date information', {'fields': ['pub_date', 'was_published_recently']})
    ]
    search_fields = ['question_text']
    list_filter = ['pub_date', 'status']
    list_display = ['question_text', 'pub_date', 'was_published_recently', 'status']
    inlines = [ChoiceInline]
    actions = ['approve_all_selected_questions', 'reject_all_selected_questions']

    @admin.action(description='Approve all selected questions')
    def approve_all_selected_questions(self, request, queryset):
        queryset.update(status=Question.Status.APPROVED)

    @admin.action(description='Reject all selected questions')
    def reject_all_selected_questions(self, request, queryset):
        queryset.update(status=Question.Status.REJECTED)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'get_question_text', 'votes']
    readonly_fields = ['votes']
    search_fields = ['choice_text', 'question__question_text']