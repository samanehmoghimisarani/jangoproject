from django.db import models
from ckeditor.fields import RichTextField


class HomeContent(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='home_content/', null=True, blank=True)
    text = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.title


