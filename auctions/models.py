from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    image_url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(null=True)
    minimum_bid_value = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="auctions_won")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="mine_auctions")

    def __str__(self):
        return f"{self.title} from {self.start_date} to {self.end_date}"

class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="mine_bids")
    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    is_active = models.BooleanField()
