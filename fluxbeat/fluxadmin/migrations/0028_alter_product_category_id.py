# Generated by Django 4.2.7 on 2024-01-20 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0027_product_offer_amount_product_offer_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_products', to='fluxadmin.category'),
        ),
    ]