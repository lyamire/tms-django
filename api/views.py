from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from polls.models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().prefetch_related('choices')
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(Question, id=question_id, status=Question.Status.APPROVED, pub_date__lte=timezone.now())
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)
