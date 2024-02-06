from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from polls.models import Question, Choice
from articles.models import Article, Author
from shop.models import Category, Product

#polls
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    # choices = ChoiceSerializer(many=True, read_only=True, required=False)
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, data):
        data['choices'] = self.initial_data.get('choices', [])
        return data

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)

        new_choices = []
        # for choice in choices:
        #     new_choices.append(Choice.objects.create(**choice))

        question.choices.set(new_choices)
        return question

#articles

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)
    class Meta:
        model = Author
        fields = '__all__'

#shop
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = '__all__'




