# Generated by Django 4.2.7 on 2023-11-30 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0008_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='verients',
            name='varient_id',
            field=models.CharField(default='a', max_length=12, unique=True),
            preserve_default=False,
        ),
    ]
