from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import connection

from advert.models import Advert, AdvertData


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT meta_id, post_id, latitude, longitude, price, sale_price, expire, urgent, sold, views, views_data, type, cond, bids, start_price, currency, exp_info "
                "FROM xdwqeiadifier_advert_data"
            )

            for row in cursor.fetchall():
                pk = row[0]
                advert_id = row[1]
                latitude = row[2]
                longitude = row[3]
                price = row[4]
                sale_price = row[5]
                expire = row[6]
                urgent = row[7]
                sold = row[8]
                views = row[9]
                views_data = row[10]
                type = row[11]
                cond = row[12]
                bids = row[13]
                start_price = row[14]
                currency = row[15]
                exp_info = row[16]

                try:
                    advert = Advert.objects.get(id=advert_id)
                    try:
                        AdvertData.objects.get(id=pk)
                    except AdvertData.DoesNotExist:
                        AdvertData.objects.create(
                            id=pk,
                            advert=advert,
                            latitude=latitude,
                            longitude=longitude,
                            price=price,
                            sale_price=sale_price,
                            expire=expire,
                            urgent=urgent,
                            sold=sold,
                            views=views,
                            views_data=views_data,
                            type=type,
                            cond=cond,
                            bids=bids,
                            start_price=start_price,
                            currency=currency,
                            exp_info=exp_info
                        )
                except Advert.DoesNotExist:
                    pass
