# Generated by Django 5.0.1 on 2024-01-03 10:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared_users',
            field=models.ManyToManyField(related_name='shared_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]