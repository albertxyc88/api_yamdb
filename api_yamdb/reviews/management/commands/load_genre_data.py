from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    # Подсказка когда пользователь пишет help.
    help = "Загрузка данных из файла category.csv"

    def handle(self, *args, **options):
        # Если данные не пустые повторно не загружаем.
        if Genre.objects.exists():
            print('Данные в genre уже загружены. Аварийное завершение.')
            return
        print('Загрузка данных в category.')
        for row in DictReader(
            open(
                './api_yamdb/static/data/genre.csv',
                encoding='utf-8-sig'
            )
        ):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()
