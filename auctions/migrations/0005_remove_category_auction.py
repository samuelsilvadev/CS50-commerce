# Generated by Django 5.1.3 on 2024-12-05 21:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="auction",
        ),
    ]
