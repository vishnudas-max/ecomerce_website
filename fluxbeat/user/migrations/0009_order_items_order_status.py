# Generated by Django 4.2.7 on 2023-12-15 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_orders_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_items',
            name='order_status',
            field=models.CharField(choices=[('Processing', 'processing'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('canceld', 'canceld')], default='Processing', max_length=20),
        ),
    ]
