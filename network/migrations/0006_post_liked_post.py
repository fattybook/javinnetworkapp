# Generated by Django 3.2.3 on 2021-06-29 02:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210626_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked_post',
            field=models.ManyToManyField(blank=True, related_name='liked_pots', to=settings.AUTH_USER_MODEL),
        ),
    ]
