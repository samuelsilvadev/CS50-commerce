from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    description = models.CharField(max_length=255, unique=True, null=False)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.pk} - {self.description}"


class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    image_url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(null=True)
    minimum_bid_value = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="auctions_won", null=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="mine_auctions"
    )
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.title} from {self.start_date} to {self.end_date}"


class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="mine_bids"
    )
    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.pk} - {self.value} - {self.date}"


class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    is_removed = models.BooleanField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()

    def __str__(self):
        return f"{self.pk} - {self.comment} - {self.date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "user", "auction", "date"],
                name="unique_comment_auction_constraint",
            )
        ]


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "auction"], name="unique_watchlist_auction_constraint"
            )
        ]
