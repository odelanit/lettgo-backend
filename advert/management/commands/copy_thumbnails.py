from django.core.management import BaseCommand
from django.db import connection

from advert.models import Advert


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT p.ID, pt.thumbnail_url FROM xdwqeiposts p LEFT JOIN (SELECT meta_value thumbnail_id, post_id FROM xdwqeipostmeta WHERE meta_key='_thumbnail_id') pm ON p.ID=pm.post_id LEFT JOIN (SELECT guid thumbnail_url, ID thumbnail_id FROM xdwqeiposts WHERE post_type='attachment') pt ON pt.thumbnail_id = pm.thumbnail_id WHERE post_type='advert';")

            for row in cursor.fetchall():
                advert_id = row[0]
                thumbnail_url = row[1]

                try:
                    advert = Advert.objects.get(id=advert_id)
                    advert.thumbnail_url = thumbnail_url
                    advert.save()
                except Advert.DoesNotExist:
                    pass
