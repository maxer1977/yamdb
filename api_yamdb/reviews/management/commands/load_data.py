from django.core.management import BaseCommand

from reviews.scripts import (load_data_genre,
                             load_data_category,
                             load_data_title,
                             load_data_user,
                             load_data_review,
                             load_data_comment)


class Command(BaseCommand):
    """
    Команда загрузки данных из csv файла в модель жанры произведений
    """

    help = 'Загрузка данных из файка genre.csv'

    def handle(self, *args, **options):
        print('\tЗагрузка данных: жанр произведений!')
        load_data_genre()
        print('\tДанные успешно загружены!\n\n'
              '\tЗагрузка данных: категория произведений!')
        load_data_category()
        print('\tДанные успешно загружены!\n\n'
              '\tЗагрузка данных: произведения!')
        load_data_title()
        print('\tДанные успешно загружены!\n\n'
              '\tЗагрузка данных: пользователи!')
        load_data_user()
        print('\tДанные успешно загружены!\n\n'
              '\tЗагрузка данных: обзоры!')
        load_data_review()
        print('\tДанные успешно загружены!\n\n'
              '\tЗагрузка данных: комментарии!')
        load_data_comment()
        print('\tЗагрузка данный завершена!')
