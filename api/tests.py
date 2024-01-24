from django.test import TestCase
from django.utils import timezone
from polls.models import Question, Choice
# Create your tests here.

class QuestionViewTests(TestCase):
    def test_emtpy_question(self):
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    def test_question_list(self):
        Question.objects.create(question_text='Text1', pub_date=timezone.now())
        Question.objects.create(question_text='Text2', pub_date=timezone.now())

        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['question_text'], 'Text1')
        self.assertEqual(data[1]['question_text'], 'Text2')

    def test_nonexistent_question_detail(self):
        response = self.client.get('/api/questions/1/')
        self.assertEqual(response.status_code, 404)

    def test_question_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())

        response = self.client.get(f'/api/questions/{question.id}/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['question_text'], question.question_text)

class ChoiceViewTests(TestCase):
    def test_emtpy_choice(self):
        response = self.client.get('/api/choices/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    def test_choice_list(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        choice_1 = question.choices.create(choice_text='Choice 1', votes=1)
        choice_2 = question.choices.create(choice_text='Choice 2', votes=1)

        response = self.client.get('/api/choices/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 2)
        data_choice_1 = next(filter(lambda x: x['choice_text'] == choice_1.choice_text, data))
        self.assertIsNotNone(data_choice_1)
        self.assertEqual(data_choice_1['votes'], choice_1.votes)
        data_choice_2 = next(filter(lambda x: x['choice_text'] == choice_2.choice_text, data))
        self.assertIsNotNone(data_choice_2)
        self.assertEqual(data_choice_2['votes'], choice_2.votes)

    def test_non_existent_choice_detail(self):
        response = self.client.get('/api/choices/1/')
        self.assertEqual(response.status_code, 404)

    def test_choice_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        choice = question.choices.create(choice_text='Choice 1', votes=1)

        response = self.client.get(f'/api/choices/{choice.id}/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['choice_text'], choice.choice_text)
        self.assertEqual(data['votes'], choice.votes)
