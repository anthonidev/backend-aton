from rest_framework import serializers
from .models import Category, Product, Brand


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        
        fields = [
            'id',
            'title',
            'is_featured',
            'photo',
            'slug',
            'description',
            'get_absolute_url'
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'title',
            'is_featured',
            'photo',
        ]


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'get_category',
#             'title',
#             'price',
#             'compare_price',
#             'is_featured',
#             'quantity',
#             'date_added',
#             'slug',
#             'num_visits',
#             'last_visit',
#             'sold',
#             'photo',
#             'get_absolute_url',
#         ]
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'id',
            'get_category',
            'title',
            'price',
            'compare_price',
            'photo',
            'slug',
            'quantity',
        ]
