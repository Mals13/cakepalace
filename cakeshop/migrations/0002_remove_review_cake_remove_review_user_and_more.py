# Generated by Django 5.1.3 on 2024-12-08 07:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeshop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='cake',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cafe',
            name='contact',
        ),
        migrations.AddField(
            model_name='cafe',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cafe',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cake',
            name='stock',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cake',
            name='cafe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeshop.cafe'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cake',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeshop.cake')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]