# Generated by Django 5.0.6 on 2024-08-10 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0008_orderitems_order_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_completion',
            field=models.BooleanField(default=False),
        ),
    ]
