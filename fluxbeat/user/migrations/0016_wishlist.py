# Generated by Django 4.2.8 on 2023-12-30 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0023_alter_coupon_offer_per'),
        ('user', '0015_alter_wallet_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateField(auto_now_add=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('proudct_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_of_wishlist', to='fluxadmin.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to=settings.AUTH_USER_MODEL)),
                ('varient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluxadmin.verients')),
            ],
        ),
    ]