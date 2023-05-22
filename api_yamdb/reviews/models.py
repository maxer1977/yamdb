from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from authorization.models import User


class Genre(models.Model):
    """Модель описывающая жанр произведения."""

    name = models.CharField(max_length=256,
                            verbose_name='Жанр')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Идентификатор жанра')

    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель описывающая категории произведений."""

    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Идентификатор категории')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель описывающая произведения."""

    name = models.CharField(max_length=256,
                            verbose_name='Названия произведения')
    year = models.PositiveSmallIntegerField(verbose_name='Год произведения')
    description = models.TextField(verbose_name='Описание',
                                   blank=True,
                                   null=True)
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='Категория произведения')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   verbose_name='Названия произведений',
                                   blank=True)

    class Meta:
        verbose_name_plural = 'Произведения'
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для обзоров от пользователей."""

    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации обзора'
    )
    text = models.TextField(verbose_name='Текст обзора')
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='not_unique_set_Reviews')
        ]

        verbose_name_plural = 'Обзоры'
        verbose_name = 'Обзор'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель для комментариев пользователей."""

    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Обзор'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )
    text = models.TextField(verbose_name='Содержание комментария')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:15]
