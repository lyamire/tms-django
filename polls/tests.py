from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.db import transaction

from .models import Question
# Create your tests here.

class QuestionModelTest(TestCase):
    def test_new_question_was_published_recently(self):
        pub_date = timezone.now() - timezone.timedelta(hours=12)
        question = Question(pub_date=pub_date)
        self.assertTrue(question.was_published_recently())

    def test_old_question_was_not_published_recently(self):
        pub_date = timezone.now() - timezone.timedelta(days=2)
        question = Question(pub_date=pub_date)
        self.assertFalse(question.was_published_recently())

    def test_future_question_was_not_published_recently(self):
        pub_date = timezone.now() + timezone.timedelta(days=2)
        question = Question(pub_date=pub_date)
        self.assertFalse(question.was_published_recently())

def create_question(question_text, days):
    pub_date = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date, status=Question.Status.APPROVED)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')

    def test_future_question_and_past_question(self):
        past_question = create_question('past', -30)
        create_question('future', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

@transaction.atomic
def create_question(raising):
    Question.objects.create(pub_date=timezone.now())
    if raising:
        raise Exception()
    Question.objects.create(pub_date=timezone.now())

class TestTransaction(TestCase):
    def test_transaction(self):
        self.assertEqual(Question.objects.count(), 0)
        create_question(False)
        self.assertEqual(Question.objects.count(), 2)
        self.assertRaises(Exception, lambda: create_question(True))
        self.assertEqual(Question.objects.count(), 2)