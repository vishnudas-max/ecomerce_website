# Generated by Django 4.2.7 on 2023-12-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_paymment_paymment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('Processing', 'processing'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('canceld', 'canceld')], default='Processing', max_length=20),
        ),
    ]
