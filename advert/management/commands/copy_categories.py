from django.core.management import BaseCommand
from django.db import connection

from advert.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT tt.term_taxonomy_id as id, if(tt.parent = 0, null, tt.parent) as parent_id, x.name, x.slug, image_url, marker_url, icon_url "
                "FROM xdwqeiterm_taxonomy tt "
                "LEFT JOIN xdwqeiterms x on tt.term_id = x.term_id "
                "LEFT JOIN (SELECT tm.meta_id, tm.meta_key, tm.meta_value, tm.term_id, p.guid as image_url "
                "FROM xdwqeitermmeta tm "
                "LEFT JOIN xdwqeiposts p on tm.meta_value = p.ID "
                "WHERE tm.meta_key = 'advert_cat_image') ci ON ci.term_id = tt.term_id "
                "LEFT JOIN (SELECT tm.meta_id, tm.meta_key, tm.meta_value, tm.term_id, p.guid as marker_url "
                "FROM xdwqeitermmeta tm "
                "LEFT JOIN xdwqeiposts p on tm.meta_value = p.ID "
                "WHERE tm.meta_key = 'advert_cat_marker') cm ON cm.term_id = tt.term_id "
                "LEFT JOIN (SELECT tm.meta_id, tm.meta_key, tm.meta_value, tm.term_id, p.guid as icon_url "
                "FROM xdwqeitermmeta tm "
                "LEFT JOIN xdwqeiposts p on tm.meta_value = p.ID "
                "WHERE tm.meta_key = 'advert_cat_icon') cc ON cc.term_id = tt.term_id "
                "WHERE taxonomy = 'advert-category' ORDER BY id")
            for row in cursor.fetchall():
                pk = row[0]
                parent_id = row[1]
                name = row[2]
                slug = row[3]
                image_url = row[4]
                marker_url = row[5]
                icon_url = row[6]
                try:
                    Category.objects.get(id=pk)
                except Category.DoesNotExist:
                    try:
                        parent = Category.objects.get(pk=parent_id)
                        Category.objects.create(
                            id=pk,
                            parent=parent, name=name, slug=slug,
                            image_url=image_url, marker_url=marker_url, icon_url=icon_url
                        )
                    except Category.DoesNotExist:
                        Category.objects.create(
                            id=pk,
                            parent=None, name=name, slug=slug,
                            image_url=image_url, marker_url=marker_url, icon_url=icon_url
                        )
