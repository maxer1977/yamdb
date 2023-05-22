from datetime import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from authorization.models import User
from reviews.models import Comment, Review, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    """Пользовательский сериализатор."""

    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role']


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать логин "me" запрещенно!'
            )
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра произведений."""

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Reviews."""

    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date',)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comments."""
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
        read_only_fields = ('pub_date',)


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        title = Review.objects.filter(title=obj.id)
        return title.aggregate(Avg('score'))['score__avg']


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведения."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if dt.today().year < value:
            raise serializers.ValidationError('Ошибка! Проверьте год!')
        return value
