from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID id, user_login username, user_pass password, user_email email, "
                "first_name, last_name, user_registered date_joined "
                "FROM xdwqeiusers u "
                "LEFT JOIN (SELECT meta_value first_name, user_id FROM xdwqeiusermeta WHERE meta_key='first_name') x "
                "ON u.ID = x.user_id "
                "LEFT JOIN (SELECT meta_value last_name, user_id FROM xdwqeiusermeta WHERE meta_key='last_name') y "
                "ON u.ID = y.user_id"
            )

            for row in cursor.fetchall():
                pk = row[0]
                username = row[1]
                password = row[2]
                email = row[3]
                first_name = row[4]
                last_name = row[5]
                date_joined = row[6]

                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    User.objects.create(
                        id=pk,
                        username=username,
                        password=password, email=email,
                        first_name=first_name, last_name=last_name,
                        date_joined=date_joined
                    )
