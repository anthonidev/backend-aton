from django.contrib import admin

from apps.product.models import Category, Product, Brand, CharacteristicProduct, ProductImage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(CharacteristicProduct)
admin.site.register(ProductImage)
