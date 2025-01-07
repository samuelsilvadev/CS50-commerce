# Generated by Django 5.1.3 on 2025-01-06 22:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0012_alter_auction_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="downvotes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="comment",
            name="is_removed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="comment",
            name="upvotes",
            field=models.IntegerField(default=0),
        ),
    ]
