# Generated by Django 4.2.7 on 2023-12-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_paymment_orders_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymment',
            name='Paymment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
