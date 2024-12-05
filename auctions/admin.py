from django.contrib import admin

from .models import Auction, User, Bid, Category, Comments, Watchlist

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Watchlist)
