from django.contrib import admin

from advert.models import Category, CategoryAdmin, Area, AreaAdmin, Advert, AdvertAdmin, Bid, BidAdmin

admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Bid, BidAdmin)
