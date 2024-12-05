from django.contrib import admin

from .models import Auction, User, Bid

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
