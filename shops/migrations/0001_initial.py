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
                ('shop_name', models.CharField(max_length=255)),
                ('shop_address', models.TextField()),
                ('shop_contact', models.CharField(max_length=20)),
                ('shop_description', models.TextField(blank=True)),
                ('shop_logo', models.ImageField(blank=True, null=True, upload_to='shop_logos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_from_shops', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]