from django.db import models
from django.conf import settings
from services.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='order_rel', null=True)
    product = models.ManyToManyField(Product, related_name='order_products')
    price = models.IntegerField(null=True)
    paid = models.BooleanField(default=False)
    total_Price = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}  '



