from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from taggit.managers import TaggableManager


class News(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='news/images/', null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    most_visited = models.SmallIntegerField(null=True, blank=True, default=0)
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    name = models.CharField(max_length=65)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=400,)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name} - {self.comment[:30]}'

    class Meta:
        ordering = ('-created',)


class Contact(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField(max_length=150)
    topic = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return f'{self.email} - {self. topic}'
