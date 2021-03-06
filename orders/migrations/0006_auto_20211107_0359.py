# Generated by Django 3.2.7 on 2021-11-07 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20211028_0111'),
        ('orders', '0005_delete_couponproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(null=True, related_name='order_products', to='services.Product'),
        ),
    ]
