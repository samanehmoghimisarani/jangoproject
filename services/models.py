from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE,
                                     related_name='category_rel_with_self', null=True, blank=True)
    is_sub = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def category_url(self):
        return reverse('services:category_filter', args=[self.slug, ])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    title = models.CharField(max_length=300, unique=True, null=True, blank=True)
    slug = models.CharField(max_length=300, unique=True)
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    pic = models.ImageField(null=True, blank=True, upload_to='example/')
    short_description = models.CharField(null=True, blank=True, max_length=200)
    description = RichTextUploadingField(null=True, blank=True)
    product_file = RichTextUploadingField(null=True, blank=True)
    most_visited = models.SmallIntegerField(null=True, blank=True, default=0)
    pay = models.BooleanField(default=False)
    tags = TaggableManager()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def price_whit_discount(self):
        if self.discount_price > 0:
            self.price = self.discount_price
            return self.price
        return self.price

    def __str__(self):
        return self.slug

    def get_short_description(self):
        return self.short_description[:50]


class ProductComment(models.Model):
    name = models.CharField(max_length=70)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.comment[:30]}'

    class Meta:
        ordering = ('-created',)


class CategoryDescription(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='category_description')
    body = RichTextUploadingField()

    def __str__(self):
        return f'{self.category.name}'
