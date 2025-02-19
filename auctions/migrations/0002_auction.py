# Generated by Django 5.1.3 on 2024-12-04 21:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=5000)),
                ("image_url", models.URLField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("is_active", models.BooleanField(null=True)),
                (
                    "minimum_bid_value",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="mine_auctions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="auctions_won",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
