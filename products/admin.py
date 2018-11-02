from django.contrib import admin

from products.models import Product, ProductComment

admin.site.register(Product)
admin.site.register(ProductComment)
