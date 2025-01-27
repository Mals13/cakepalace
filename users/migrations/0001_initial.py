# Generated by Django 5.1.3 on 2024-12-08 17:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15)),
                ('is_approved', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_from_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
