import urllib.request

from django.core.management import BaseCommand

from advert.models import Advert


class Command(BaseCommand):
    def handle(self, *args, **options):
        adverts = Advert.objects.all()
        for advert in adverts:
            thumbnail_url = advert.thumbnail_url
            # print(thumbnail_url)
            filename = thumbnail_url.replace("https://www.lettgo.no/wp-content/uploads/", "")
            urllib.request.urlretrieve(advert.thumbnail_url, "uploads/" + filename)
            advert.thumbnail.name = filename
            # print(filename)
            advert.save()
