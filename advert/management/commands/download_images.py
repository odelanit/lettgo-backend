import urllib.request

from django.core.management import BaseCommand

from advert.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = Category.objects.all()
        for category in categories:
            icon_url = category.icon_url
            image_url = category.image_url
            marker_url = category.marker_url
            if icon_url:
                filename = icon_url.replace("https://www.lettgo.no/wp-content/uploads/", "")
                urllib.request.urlretrieve(category.icon_url, "uploads/" + filename)
                category.icon.name = filename
            if image_url:
                filename = image_url.replace("https://www.lettgo.no/wp-content/uploads/", "")
                urllib.request.urlretrieve(category.image_url, "uploads/" + filename)
                category.image.name = filename
            if marker_url:
                filename = icon_url.replace("https://www.lettgo.no/wp-content/uploads/", "")
                urllib.request.urlretrieve(category.marker_url, "uploads/" + filename)
                category.marker.name = filename
            category.save()
