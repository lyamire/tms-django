from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .forms import QuestionForm
from .models import Question, Choice
from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(status=Question.Status.APPROVED).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    # model = Question
    template_name = "polls/detail.html"

    def get_object(self, queryset=None):
        return Question.objects.filter(status=Question.Status.APPROVED).get(id=self.kwargs['pk'])


def vote(request, question_id: int):
    question = get_object_or_404(Question, id=question_id, status=Question.Status.APPROVED)
    try:
        selected_choice = question.choices.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'error_message': "You didn't select a choice",
            'question': question,
        })
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('polls:results', question.id)

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            pub_date = form.cleaned_data['publication_date']
            question = Question(question_text=question_text, pub_date=pub_date)
            question.save()
            for choice_text in form.cleaned_data['choices'].split('\n'):
                question.choices.create(choice_text=choice_text, votes=0)
            return redirect('polls:detail', question.id)
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})
