# Generated by Django 4.2.7 on 2024-01-23 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_referal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to=settings.AUTH_USER_MODEL),
        ),
    ]
