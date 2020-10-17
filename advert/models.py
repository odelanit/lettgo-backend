from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    image_url = models.CharField(blank=True, null=True, max_length=255)
    marker_url = models.CharField(blank=True, null=True, max_length=255)
    icon_url = models.CharField(blank=True, null=True, max_length=255)

    parent = models.ForeignKey("Category", related_name="_children", null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['parent_id']

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

    def icon_tag(self):
        if self.icon_url:
            return mark_safe('<img src="%s" />' % self.icon_url)
        else:
            return '-'
    icon_tag.short_description = 'Icon'

    def image_tag(self):
        if self.image_url:
            return mark_safe('<img src="%s" />' % self.image_url)
        else:
            return '-'
    image_tag.short_description = 'Image'

    def marker_tag(self):
        if self.marker_url:
            return mark_safe('<img src="%s" />' % self.marker_url)
        else:
            return '-'
    marker_tag.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'icon_tag', 'image_tag', 'marker_tag',)
    readonly_fields = ('icon_tag', 'image_tag', 'marker_tag',)


class Area(models.Model):
    name = models.CharField(max_length=191)
    slug = models.CharField(max_length=191, unique=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=191, blank=True, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)

    parent = models.ForeignKey("Area", related_name='children', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['parent_id', 'name']

    def __str__(self):
        return self.name


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description', 'parent',)


class Advert(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('publish', 'Publish')
    ]
    title = models.CharField(max_length=191)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=64, default='publish')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AdvertAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'user',
        'created_at',
        'updated_at'
    )


class AdvertData(models.Model):
    advert = models.OneToOneField(Advert, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    expire = models.BigIntegerField(null=True)
    urgent = models.BigIntegerField(null=True)
    sold = models.IntegerField(null=True)
    views = models.IntegerField(null=True)
    views_data = models.TextField(null=True)
    type = models.IntegerField(null=True)
    cond = models.IntegerField(null=True)
    bids = models.IntegerField(null=True)
    start_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    currency = models.CharField(max_length=5, null=True)
    exp_info = models.CharField(max_length=1, default='0', null=True)


class AdvertDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'advert',
        'latitude', 'longitude',
        'price', 'sale_price',
        'expire', 'urgent', 'sold',
        'views', 'views_data',
        'type', 'cond', 'bids', 'start_price', 'currency',
        'exp_info'
    )


class Bid(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=20, decimal_places=2)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'advert', 'user', 'bid', 'ip', 'created_at',)


class Conversation(models.Model):
    advert_title = models.TextField()
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send_conversations")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recv_conversations")
    sender_delete = models.IntegerField(null=True)
    recipient_delete = models.IntegerField(null=True)
    last_message_id = models.BigIntegerField(null=True)
    sender_review = models.IntegerField(null=True)
    recipient_review = models.IntegerField(null=True)
    invert_review = models.IntegerField(null=True)


class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'advert',
        'sender', 'recipient',
        'sender_delete', 'recipient_delete',
        'last_message_id',
        'sender_review', 'recipient_review',
        'invert_review'
    )


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    source_id = models.BigIntegerField(null=True)
    message = models.TextField(null=True)
    is_read = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'source_id', 'message', 'is_read', 'created_at')


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send_reviews")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recv_reviews")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    review = models.TextField()
    rating = models.IntegerField(1)
    advert_title = models.TextField()
    is_seller = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('Review', on_delete=models.CASCADE, related_name="children")


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'reviewer', 'reviewed',
        'conversation',
        'review', 'rating',
        'advert_title',
        'is_seller',
        'created_at',
        'parent'
    )
