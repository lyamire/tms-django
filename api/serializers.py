from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from polls.models import Question, Choice
from articles.models import Article, Author
from shop.models import Category, Order, OrderEntry, Product


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password'
        ]
        validators = [
            UniqueTogetherValidator(queryset=User.objects.all(), fields=['email']),
            UniqueTogetherValidator(queryset=User.objects.all(), fields=['username']),
        ]

    def validate(self, data):
        if data['password'] != self.initial_data.get('password2', None):
            raise serializers.ValidationError('Password wrong')
        return data


# polls
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


# articles

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)

    class Meta:
        model = Author
        fields = '__all__'


# shop
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        include_products = self.context['request'].query_params.get('include_products', 'true')
        if include_products == 'false' and 'products' in self.fields:
            self.fields.pop('products')
        return super().to_representation(obj)

    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class OrderEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEntry
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_entries = OrderEntrySerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    remove = serializers.BooleanField(required=False, default=False)
    count = serializers.IntegerField(required=False, default=None, allow_null=True)


class UpdateOrderSerializer(serializers.Serializer):
    clear = serializers.BooleanField(required=False, default=False)
    order_entries = UpdateOrderEntrySerializer(many=True, read_only=False, default=[])

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
        ]
        read_only_fields = ['id', 'username']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
