# Generated by Django 4.2.7 on 2023-11-30 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0012_brand_brand_date_category_cat_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='cat_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='verients',
            name='varient_date',
            field=models.DateField(blank=True),
        ),
    ]
