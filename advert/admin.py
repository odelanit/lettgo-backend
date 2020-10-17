from django.contrib import admin

from advert.models import Category, CategoryAdmin, Area, AreaAdmin, Advert, AdvertAdmin, Bid, BidAdmin, AdvertDataAdmin, \
    AdvertData, Conversation, ConversationAdmin, ConversationMessage, ConversationMessageAdmin, ReviewAdmin, Review

admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(AdvertData, AdvertDataAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationMessage, ConversationMessageAdmin)
admin.site.register(Review, ReviewAdmin)
