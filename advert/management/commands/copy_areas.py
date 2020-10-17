from django.core.management import BaseCommand
from django.db import connection

from advert.models import Area


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT tt.term_taxonomy_id as id, "
                "x.name, tt.description, x.slug, if(tt.parent = 0, null, tt.parent) as parent_id "
                "FROM xdwqeiterm_taxonomy tt "
                "LEFT JOIN xdwqeiterms x on tt.term_id = x.term_id "
                "WHERE taxonomy = 'advert-location'")
            for row in cursor.fetchall():
                pk = row[0]
                name = row[1]
                description = row[2]
                slug = row[3]
                parent_id = row[4]

                try:
                    Area.objects.get(id=pk)
                except Area.DoesNotExist:
                    try:
                        parent = Area.objects.get(pk=parent_id)
                        Area.objects.create(
                            id=pk, name=name, description=description, slug=slug, parent=parent
                        )
                    except Area.DoesNotExist:
                        Area.objects.create(
                            id=pk, name=name, description=description, slug=slug, parent=None
                        )
                    pass
