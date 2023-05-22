from csv import DictReader

from django.db.utils import IntegrityError

from authorization.models import User
from reviews.models import Category, Genre, Title, Comment, Review


def load_data_genre():
    """Загрузка жанра произведений в базу данных."""

    for row in DictReader(open('static/data/genre.csv')):
        Genre.objects.get_or_create(id=row['id'],
                                    name=row['name'],
                                    slug=row['slug'])


def load_data_category():
    """Загрузка категории произведений в базу данных."""

    for row in DictReader(open('static/data/category.csv')):
        Category.objects.get_or_create(
            id=row['id'], name=row['name'], slug=row['slug']
        )


def load_data_title():
    """Загрузка произведений в базу данных."""

    for row in DictReader(open('static/data/titles.csv')):
        Title.objects.get_or_create(id=row['id'],
                                    name=row['name'],
                                    year=row['year'],
                                    category_id=row['category'])
    for row in DictReader(open('static/data/genre_title.csv')):
        Title.objects.get(id=row['title_id']).genre.add(row['genre_id'])


def load_data_user():
    """Загрузка пользователей в базу данных."""

    for row in DictReader(open('static/data/users.csv')):
        User.objects.get_or_create(id=row['id'],
                                   username=row['username'],
                                   email=row['email'],
                                   role=row['role'],
                                   bio=row['bio'],
                                   first_name=row['first_name'],
                                   last_name=row['last_name'])


def load_data_review():
    """Загрузка обзоров в базу данных."""

    for row in DictReader(open('static/data/review.csv')):
        try:
            Review.objects.get_or_create(id=row['id'],
                                         title_id=row['title_id'],
                                         text=row['text'],
                                         author_id=row['author'],
                                         score=row['score'],
                                         pub_date=row['pub_date'])
        except IntegrityError:
            pass


def load_data_comment():
    """Загрузка комментариев в базу данных."""

    for row in DictReader(open('static/data/comments.csv')):
        try:
            Comment.objects.get_or_create(id=row['id'],
                                          review_id=row['review_id'],
                                          text=row['text'],
                                          author_id=row['author'],
                                          pub_date=row['pub_date'])
        except IntegrityError:
            pass
