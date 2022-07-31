import os

from csv import DictReader
from django.core.management import BaseCommand
from django.conf import settings

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title)
from users.models import User


category_file = os.path.join(
    settings.BASE_DIR,
    'static/data/category.csv'
)
comments_file = os.path.join(
    settings.BASE_DIR,
    'static/data/comments.csv'
)
genre_file = os.path.join(
    settings.BASE_DIR,
    'static/data/genre.csv'
)
genre_title_file = os.path.join(
    settings.BASE_DIR,
    'static/data/genre_title.csv'
)
review_file = os.path.join(
    settings.BASE_DIR,
    'static/data/review.csv'
)
titles_file = os.path.join(
    settings.BASE_DIR,
    'static/data/titles.csv'
)
users_file = os.path.join(
    settings.BASE_DIR,
    'static/data/users.csv'
)


class Command(BaseCommand):
    # Подсказка когда пользователь пишет help.
    help = "Загрузка данных в базу данных из файлов *.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            action='store_true',
            help='Загрузка данных в базу данных из файла category.csv'
        )
        parser.add_argument(
            '--comments',
            action='store_true',
            help='Загрузка данных в базу данных из файла comments.csv'
        )
        parser.add_argument(
            '--genre_title',
            action='store_true',
            help='Загрузка данных в базу данных из файла genre_title.csv'
        )
        parser.add_argument(
            '--genre',
            action='store_true',
            help='Загрузка данных в базу данных из файла genre.csv'
        )
        parser.add_argument(
            '--review',
            action='store_true',
            help='Загрузка данных в базу данных из файла review.csv'
        )
        parser.add_argument(
            '--titles',
            action='store_true',
            help='Загрузка данных в базу данных из файла titles.csv'
        )
        parser.add_argument(
            '--users',
            action='store_true',
            help='Загрузка данных в базу данных из файла users.csv'
        )
        parser.add_argument(
            '--import_all',
            action='store_true',
            help='Загрузка данных в базу данных во все таблицы.'
        )

    def import_category(self):
        # Если данные не пустые повторно не загружаем.
        if Category.objects.exists():
            print('Данные в category уже загружены. Аварийное завершение.')
        else:
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
            print('Загрузка данных в category завершена.')

    def import_comments(self):
        # Если данные не пустые повторно не загружаем.
        if Comment.objects.exists():
            print('Данные в comments уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в comments.')
            for row in DictReader(
                open(
                    comments_file,
                    encoding='utf-8-sig'
                )
            ):
                comments = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                comments.save()
            print('Загрузка данных в comments завершена.')

    def import_genre(self):
        # Если данные не пустые повторно не загружаем.
        if Genre.objects.exists():
            print('Данные в genre уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в genre.')
            for row in DictReader(
                open(
                    genre_file,
                    encoding='utf-8-sig'
                )
            ):
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()
            print('Загрузка данных в genre завершена.')

    def import_genre_title(self):
        # Если данные не пустые повторно не загружаем.
        if GenreTitle.objects.exists():
            print('Данные в genre_title уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в genre_title.')
            for row in DictReader(
                open(
                    genre_title_file,
                    encoding='utf-8-sig'
                )
            ):
                genre_title = GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                genre_title.save()
            print('Загрузка данных в genre_title завершена.')

    def import_review(self):
        # Если данные не пустые повторно не загружаем.
        if Review.objects.exists():
            print('Данные в review уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в review.')
            for row in DictReader(
                open(
                    review_file,
                    encoding='utf-8-sig'
                )
            ):
                review = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                review.save()
            print('Загрузка данных в review завершена.')

    def import_titles(self):
        # Если данные не пустые повторно не загружаем.
        if Title.objects.exists():
            print('Данные в title уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в title.')
            for row in DictReader(
                open(
                    titles_file,
                    encoding='utf-8-sig'
                )
            ):
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category'])
                )
                title.save()
            print('Загрузка данных в title завершена.')

    def import_users(self):
        # Если данные не пустые повторно не загружаем.
        if User.objects.exists():
            print('Данные в users уже загружены. Аварийное завершение.')
        else:
            print('Загрузка данных в users.')
            for row in DictReader(
                open(
                    users_file,
                    encoding='utf-8-sig'
                )
            ):
                users = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                users.save()
            print('Загрузка данных в users завершена.')

    def handle(self, **options):
        if options['category']:
            self.import_category()
        if options['comments']:
            self.import_comments()
        if options['genre_title']:
            self.import_genre_title()
        if options['genre']:
            self.import_genre()
        if options['review']:
            self.import_review()
        if options['titles']:
            self.import_titles()
        if options['users']:
            self.import_users()
        if options['import_all']:
            self.import_users()
            self.import_genre()
            self.import_category()
            self.import_titles()
            self.import_genre_title()
            self.import_review()
            self.import_comments()
