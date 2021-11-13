from django.contrib import admin
from .models import Product, Category, CategoryDescription , ProductComment


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductComment)
admin.site.register(CategoryDescription)

