# Generated by Django 5.1.3 on 2024-12-09 22:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_rename_comments_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='auctions_won', to=settings.AUTH_USER_MODEL),
        ),
    ]