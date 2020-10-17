from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import connection

from advert.models import Advert


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID, post_title, post_content, post_author, post_status, post_date, post_modified "
                "FROM xdwqeiposts p "
                "WHERE post_type='advert';"
            )

            for row in cursor.fetchall():
                pk = row[0]
                title = row[1]
                description = row[2]
                user_id = row[3]
                status = row[4]
                created_at = row[5]
                updated_at = row[6]

                try:
                    Advert.objects.get(pk=pk)
                except Advert.DoesNotExist:
                    try:
                        user = User.objects.get(id=user_id)
                        Advert.objects.create(
                            id=pk,
                            title=title,
                            description=description,
                            user=user,
                            status=status,
                            created_at=created_at,
                            updated_at=updated_at
                        )
                    except User.DoesNotExist:
                        pass
