# Generated by Django 4.2.7 on 2023-11-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxadmin', '0010_alter_verients_varient_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]