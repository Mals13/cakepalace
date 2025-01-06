# Generated by Django 5.1.3 on 2024-12-18 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0005_rename_user_order_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Confirmed', 'Confirmed'), ('Out for Delivery', 'Out for Delivery'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
