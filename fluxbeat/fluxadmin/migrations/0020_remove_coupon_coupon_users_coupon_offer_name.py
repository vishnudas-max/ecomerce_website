# Generated by Django 4.2.8 on 2023-12-22 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0019_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='coupon_users',
        ),
        migrations.AddField(
            model_name='coupon',
            name='offer_name',
            field=models.CharField(default=2, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
