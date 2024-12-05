from django.contrib import admin

from .models import Auction, User

admin.site.register(User)
admin.site.register(Auction)
