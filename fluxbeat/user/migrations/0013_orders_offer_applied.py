# Generated by Django 4.2.8 on 2023-12-22 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0022_coupon'),
        ('user', '0012_orders_discount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='offer_applied',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offer_applied_orders', to='fluxadmin.coupon'),
        ),
    ]
