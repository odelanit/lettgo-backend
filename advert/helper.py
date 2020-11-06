from django.utils import timezone


def image_directory_path(instance, filename):
    now = timezone.now()
    return '{0}/{1}/{2}'.format(now.year, now.month, filename)
