from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    active_date_start = models.DateTimeField(null=True, blank=True)
    active_date_end = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.code} . {self.active} '





