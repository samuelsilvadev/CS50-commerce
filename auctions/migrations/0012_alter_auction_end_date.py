# Generated by Django 5.1.3 on 2024-12-09 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_auction_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
    ]
