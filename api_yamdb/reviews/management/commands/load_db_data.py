from csv import DictReader
from django.core.management import BaseCommand
from django.conf import settings

from reviews.models import (Category, Comment, Genre, GenreTitle, Review, 
                            Title, User)

print(settings.BASE_DIR)
category_file = './api_yamdb/static/data/category.csv'



class Command(BaseCommand):
    # Подсказка когда пользователь пишет help.
    help = "Загрузка данных в базу данных из файлов *.csv"

    def add_arguments(self, parser):
        parser.add_argument(
        '-c', 
        '--category',
        action='store', 
        default=False,
        help='Загрузка данных category.csv в БД.'
        )

    def handle(self, *args, **options):
        # Если данные не пустые повторно не загружаем.
        if Category.objects.exists():
            print('Данные в category уже загружены. Аварийное завершение.')
            return
        print('Загрузка данных в category.')
        for row in DictReader(
            open(
                category_file,
                encoding='utf-8-sig'
            )
        ):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()
