from django.contrib import admin

from .models import Auction, User, Bid, Category, Comments

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comments)
