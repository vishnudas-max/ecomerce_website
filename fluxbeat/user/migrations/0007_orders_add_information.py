# Generated by Django 4.2.7 on 2023-12-14 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_orders_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='add_information',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]