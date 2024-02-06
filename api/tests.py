from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question, Choice
from articles.models import Article, Author
from shop.models import Category, Product
# Create your tests here.

#polls
class QuestionViewTests(TestCase):
    def test_emtpy_question(self):
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(data, [])

    def test_create_question(self):
        data = {
            "question_text": "What's the meaning of the word 'meaningless'?",
            "pub_date": "2024-01-31T11:42:16.621314Z",
            "status": "AP",
            "choices": [
                {
                    "choice_text": "Full of meaning",
                    "votes": 3
                },
                {
                    "choice_text": "Full of meaning 2 ",
                    "votes": 42
                },
            ]
        }

        response = self.client.post('/api/questions/', data)
        response_data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['question_text'], data['question_text'])
        entity = Question.objects.get(pk=response_data['id'])
        self.assertEqual(entity.question_text, data['question_text'])
        # self.assertTrue(entity.choices)

    def test_question_list(self):
        Question.objects.create(question_text='Text1', pub_date=timezone.now())
        Question.objects.create(question_text='Text2', pub_date=timezone.now())

        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
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

    def test_search_question(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())

        response = self.client.get('/api/questions/?search=Text1')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertTrue(len(data))
        for item in data:
            self.assertEqual(item['question_text'], question.question_text)

    def test_filter_question(self):
        Question.objects.create(question_text='Text2', pub_date=timezone.datetime(2006, 6, 1))
        Question.objects.create(question_text='Text3', pub_date=timezone.datetime(2007, 6, 1))
        Question.objects.create(question_text='Text1', pub_date=timezone.datetime(2005, 6, 1))

        response = self.client.get('/api/questions/?ordering=pub_date')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['question_text'], 'Text1')
        self.assertEqual(data[1]['question_text'], 'Text2')
        self.assertEqual(data[2]['question_text'], 'Text3')

    def test_pagination_questions(self):
        Question.objects.create(question_text='Text1', pub_date=timezone.now())
        Question.objects.create(question_text='Text2', pub_date=timezone.now())
        Question.objects.create(question_text='Text3', pub_date=timezone.now())

        response = self.client.get('/api/questions/?page=2&page_size=1')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertTrue(data['next'].endswith('/api/questions/?page=3&page_size=1'))
        self.assertTrue(data['previous'].endswith('/api/questions/?page_size=1'))
        self.assertTrue(data['results'])

    def test_min_choice_count(self):
        question_1 = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        choice_1 = question_1.choices.create(choice_text='Choice 1', votes=1)
        choice_2 = question_1.choices.create(choice_text='Choice 2', votes=1)
        question_2 = Question.objects.create(question_text='Text2', pub_date=timezone.now())
        choice_3 = question_2.choices.create(choice_text='Choice 3', votes=1)
        choice_4 = question_2.choices.create(choice_text='Choice 4', votes=1)
        choice_5 = question_2.choices.create(choice_text='Choice 5', votes=1)

        response = self.client.get('/api/questions/?min_choice_count=3')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results'][0]['choices']
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['choice_text'], choice_3.choice_text)
        self.assertEqual(data[1]['choice_text'], choice_4.choice_text)
        self.assertEqual(data[2]['choice_text'], choice_5.choice_text)

    def test_max_choice_count(self):
        question_1 = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        choice_1 = question_1.choices.create(choice_text='Choice 1', votes=1)
        choice_2 = question_1.choices.create(choice_text='Choice 2', votes=1)
        question_2 = Question.objects.create(question_text='Text2', pub_date=timezone.now())
        choice_3 = question_2.choices.create(choice_text='Choice 3', votes=1)
        choice_4 = question_2.choices.create(choice_text='Choice 4', votes=1)
        choice_5 = question_2.choices.create(choice_text='Choice 5', votes=1)

        response = self.client.get('/api/questions/?max_choice_count=2')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results'][0]['choices']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['choice_text'], choice_1.choice_text)
        self.assertEqual(data[1]['choice_text'], choice_2.choice_text)




class ChoiceViewTests(TestCase):
    def test_emtpy_choice(self):
        response = self.client.get('/api/choices/')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertEqual(data, [])

    def test_choice_list(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        choice_1 = question.choices.create(choice_text='Choice 1', votes=1)
        choice_2 = question.choices.create(choice_text='Choice 2', votes=1)

        response = self.client.get('/api/choices/')

        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
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

    def test_choice_vote(self):
        # Arrange
        question = Question.objects.create(question_text='Text1',
                                           pub_date=timezone.now(),
                                           status=Question.Status.APPROVED)
        choice = question.choices.create(choice_text='Choice 1', votes=1)
        data = {
            'choice': choice.id
        }
        question.save()

        # Act
        response = self.client.post(f'/api/questions/{question.id}/vote', data)

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/api/questions/{question.id}/')

#articles
class ArticleViewTests(TestCase):
    data = {
        "title": "Курица в подарок",
        "text": "Пригласили на техническое собеседование старшего Java-разработчика, предложили провести его в онлайн-формате, но получили от соискателя твёрдый отказ, так как он хотел увидеть офис, «посмотреть в глаза техлиду» и пообщаться по душам. К слову, вакансия удалённая. В назначенное время мы встретили кандидата в нашем московском офисе. Первое, что нас удивило, это ленты под бейджик с логотипами Мэйл.ру и Яндекса на шее у соискателя, а сверху лента с лого нашей компании. Видимо, мы были уже третьей компанией, в которой он проходил интервью в этот день. Второй момент, который нас заинтересовал — соискатель пришел на собеседование с переноской для кошек, аккуратно поставил её в углу переговорки и, казалось бы, забыл про неё. Началось собеседование, которое кандидат блестяще прошёл, ответив на все логические и технические вопросы. Он оказался приятным и грамотным специалистом. После собеседования я предложила показать ему офис и напоить водичкой его «котёнка». Сначала он явно меня не понял, а потом радостно поставил на большой стол переноску, открыл её и достал оттуда живую курицу, которая смело пошла по нашим бумагам, корпоративными презентациям и трифолдам! Все просто остолбенели. Не замечая нашей реакции, соискатель сказал, что он решил подарить курицу будущему работодателю и теперь она наша. Такой паники и восторга одновременно я не испытала ни на одном собеседовании в своей жизни, а наш технический специалист так откровенно ржал впервые.",
        "like_count": 0,
        "status": "AP"
    }

    def test_empty_article(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(data, [])

    def test_article_list(self):
        Article.objects.create(title='article 1')
        Article.objects.create(title='article 2')
        Article.objects.create(title='article 3')

        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['title'], 'article 1')
        self.assertEqual(data[1]['title'], 'article 2')
        self.assertEqual(data[2]['title'], 'article 3')

    def test_nonexistent_article_detail(self):
        response = self.client.get('/api/articles/100/')
        self.assertEqual(response.status_code, 404)

    def test_article_detail(self):
        article = Article.objects.create(title='Text_1')

        response = self.client.get(f'/api/articles/{article.id}/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['title'], article.title)

    def test_create_article(self):
        response = self.client.post(f'/api/articles/', self.data)

        self.assertEqual(response.status_code, 201)
        self.compare_article_with_data(response.data['id'], self.data)

        self.assertEqual(response.data["title"], self.data["title"])
        self.assertEqual(response.data["text"], self.data["text"])
        self.assertEqual(response.data["like_count"], self.data["like_count"])
        self.assertEqual(response.data["status"], self.data["status"])

    def test_update_article(self):
        article_old = Article.objects.create(
            title="sdfsd fsfsdfs dsd fsd f sdfs ",
            text="ksdkjhs ksdjhksjdh kjsdksjdk jfh skdjhf",
            like_count=42,
            status="IN"
        )

        response = self.client.put(f'/api/articles/{article_old.id}/', self.data, 'application/json')

        self.assertEqual(response.status_code, 200)
        self.compare_article_with_data(article_old.id, self.data)

    def compare_article_with_data(self, article_id, data):
        article = Article.objects.get(id=article_id)
        self.assertIsNotNone(article)

        self.assertEqual(data["title"], article.title)
        self.assertEqual(data["text"], article.text)
        self.assertEqual(data["like_count"], article.like_count)
        self.assertEqual(data["status"], article.status)

    def test_delete_article(self):
        article_old = Article.objects.create(
            title="sdfsd fsfsdfs dsd fsd f sdfs ",
            text="ksdkjhs ksdjhksjdh kjsdksjdk jfh skdjhf",
            like_count=42,
            status="IN"
        )

        response = self.client.delete(f'/api/articles/{article_old.id}/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Exception):
            Article.objects.get(id=article_old.id)

class AuthorViewTest(TestCase):
    def test_author_empty(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(data, [])

    def test_author_list(self):
        Author.objects.create(first_name='name_1', last_name='last_name_1', date_of_birth='2011-11-11')
        Author.objects.create(first_name='name_2', last_name='last_name_2', date_of_birth='2012-12-12')

        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['first_name'], 'name_1')
        self.assertEqual(data[0]['last_name'], 'last_name_1')
        self.assertEqual(data[0]['date_of_birth'], '2011-11-11')
        self.assertEqual(data[1]['first_name'], 'name_2')
        self.assertEqual(data[1]['last_name'], 'last_name_2')
        self.assertEqual(data[1]['date_of_birth'], '2012-12-12')

    def test_nonexistent_author_detail(self):
        response = self.client.get('/api/authors/100/')
        self.assertEqual(response.status_code, 404)

    def test_author_detail(self):
        author = Author.objects.create(first_name='name_1', last_name='last_name_1', date_of_birth='2011-11-11')
        response = self.client.get(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['first_name'], 'name_1')
        self.assertEqual(data['last_name'], 'last_name_1')
        self.assertEqual(data['date_of_birth'], '2011-11-11')

#shop
class CategoryViewTest(TestCase):
    def test_category_empty(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(data, [])

    def test_category_list(self):
        Category.objects.create(name='Test 1')
        Category.objects.create(name='Test 2')
        Category.objects.create(name='Test 3')

        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['name'], 'Test 1')
        self.assertEqual(data[1]['name'], 'Test 2')
        self.assertEqual(data[2]['name'], 'Test 3')

    def test_nonexistent_category(self):
        response = self.client.get('/api/categories/100/')
        self.assertEqual(response.status_code, 404)

    def test_category_detail(self):
        category = Category.objects.create(name='Test 1')
        response = self.client.get(f'/api/categories/{category.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Test 1')

class ProductViewTest(TestCase):
    def test_product_empty(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(data, [])

    def test_product_list(self):
        category = Category.objects.create(name='Test 1')
        Product.objects.create(name='Test 1', category_id=category.id)
        Product.objects.create(name='Test 2', category_id=category.id)

        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)

        data = response.json()['results']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Test 1')
        self.assertEqual(data[1]['name'], 'Test 2')

    def test_nonexistent_product(self):
        response = self.client.get('/api/products/1000/')
        self.assertEqual(response.status_code, 404)

    def test_product_detail(self):
        category = Category.objects.create(name='Test 1')
        product = Product.objects.create(name='Test 1', category_id=category.id)
        response = self.client.get(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Test 1')
