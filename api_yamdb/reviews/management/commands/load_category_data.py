from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    # Подсказка когда пользователь пишет help.
    help = "Загрузка данных из файла category.csv"

    def handle(self, *args, **options):
        # Если данные не пустые повторно не загружаем.
        if Category.objects.exists():
            print('Данные в category уже загружены. Аварийное завершение.')
            return
        print('Загрузка данных в category.')
        for row in DictReader(
            open(
                './api_yamdb/static/data/category.csv',
                encoding='utf-8-sig'
            )
        ):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()
