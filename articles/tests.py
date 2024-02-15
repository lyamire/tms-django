from django.test import TestCase
from django.urls import reverse
from .models import Article
# Create your tests here.

def create_article(title):
    return Article.objects.create(title=title, text=title, status=Article.Status.APPROVED)

class ArticleIndexTests(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse('articles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no articles')

    def test_articles(self):
        test_1 = create_article('Test 1')
        test_2 = create_article('Test 2')
        test_3 = create_article('Test 3')
        response = self.client.get(reverse('articles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['articles'].order_by("title"), [test_1, test_2, test_3])

class ArticleDetailTests(TestCase):
    def test_article_not_exists(self):
        response = self.client.get(reverse('articles:detail', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_article_detail(self):
        article = create_article('Test')
        response = self.client.get(reverse('articles:detail', args=[article.id]))
        self.assertContains(response, article.title)

class ArticleModelTests(TestCase):
    def test_like_count_lt_100(self):
        article = Article(like_count=99)
        self.assertFalse(article.is_popular())

    def test_like_count_eq_100(self):
        article = Article(like_count=100)
        self.assertFalse(article.is_popular())

    def test_like_count_gt_100(self):
        article = Article(like_count=101)
        self.assertTrue(article.is_popular())
