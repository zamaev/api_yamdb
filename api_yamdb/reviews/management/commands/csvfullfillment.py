import csv
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, GenreTitle

CSV_FILES = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle
}

ID_FIELDS = {
    'category': Category,
}


class Command(BaseCommand):
    help = 'Fullfills the DB with data from csv files'

    def handle(self, *args, **options):
        for file_name, model in CSV_FILES.items():
            with open('static/data/' + file_name, encoding='utf-8') as file:
                data = csv.DictReader(file)
                for row in data:
                    for key, value in row.items():
                        if key in ID_FIELDS:
                            row[key] = ID_FIELDS[key].objects.get(pk=value)
                    model.objects.create(**row)
