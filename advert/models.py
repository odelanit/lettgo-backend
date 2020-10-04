from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from advert.helper import image_directory_path


class Category(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.CharField(blank=True, null=True, max_length=255)
    marker_url = models.CharField(blank=True, null=True, max_length=255)
    icon_url = models.CharField(blank=True, null=True, max_length=255)

    parent = models.ForeignKey("Category", related_name="_children", null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @property
    def _showChildren(self):
        return True

    @property
    def label(self):
        return self.name

    @property
    def children(self):
        return self._children.all()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')


class Area(models.Model):
    name = models.CharField(max_length=191)
    address = models.CharField(max_length=191, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, default=0)

    parent = models.ForeignKey("Area", related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address',)


class Advert(models.Model):
    title = models.CharField(max_length=191)
    description = models.TextField()

    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2)
    expire = models.BigIntegerField()
    urgent = models.BigIntegerField()
    sold = models.BooleanField()
    views = models.IntegerField()
    views_data = models.TextField()
    type = models.IntegerField()
    cond = models.IntegerField()
    bids = models.IntegerField(default=0)
    start_price = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=5)
    exp_info = models.CharField(max_length=1, default='0')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AdvertAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'price',
        'sale_price',
        'expire',
        'urgent',
        'sold',
        'views',
        'type',
        'cond',
        'bids',
        'start_price'
    )


class Bid(models.Model):
    bid = models.DecimalField(max_digits=20, decimal_places=2)
    ip = models.GenericIPAddressField()
    created = models.BigIntegerField()

    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid', 'ip', 'created', 'advert', 'user')


class Conversation(models.Model):
    advert_title = models.TextField()

    # TODO: sender_delete, recipient_delete, last_message, sender_review, recipient_review, invert_review

    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send_conversations")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recv_conversations")


class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField(1)
    advert_title = models.TextField()
    is_seller = models.BooleanField()
    created = models.BigIntegerField()

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send_reviews")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recv_reviews")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    parent = models.ForeignKey('Review', on_delete=models.CASCADE, related_name="children")


# TODO: adifier_cf_groups, adifier_cf, adifier_conversation_messages
