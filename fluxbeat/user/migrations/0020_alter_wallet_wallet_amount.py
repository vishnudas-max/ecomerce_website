# Generated by Django 4.2.7 on 2024-01-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_order_items_return_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]