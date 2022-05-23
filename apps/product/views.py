
from cmath import log
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Category, CharacteristicProduct, Product, Brand, ProductImage
from .serializers import CategorySerializer, CharacteristicProductSerializer, ProductImageSerializer, ProductSerializer, BrandSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import random


class ListBrandView(generics.ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None

    def get(self, request, format=None, *args, **kwargs):
        queryset = Brand.objects.all()
        return Response({'brands': self.serializer_class(queryset, many=True).data}, status=status.HTTP_200_OK)


class ListCategoryView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        print(products.count())
        result = []

        for category in categories:
            if not category.parent:
                total = products.filter(category=category).count()
                item = {}
                item['id'] = category.id
                item['title'] = category.title
                item['photo'] = category.photo
                item['slug'] = category.slug
                item['description'] = category.description
                item['total'] = total
                item['sub_categories'] = []
                for cat in categories:
                    sub_item = {}
                    total = products.filter(category=cat).count()
                    if cat.parent and cat.parent.id == category.id:
                        sub_item['id'] = cat.id
                        sub_item['title'] = cat.title
                        sub_item['photo'] = cat.photo
                        sub_item['sub_categories'] = []
                        sub_item['slug'] = cat.slug
                        sub_item['description'] = cat.description
                        sub_item['total'] = total
                        item['sub_categories'].append(sub_item)
                result.append(item)
        return Response({'categories': result}, status=status.HTTP_200_OK)


class ListProductHomeView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None, *args, **kwargs):
        products = Product.objects.filter(is_featured=True)
        page = self.paginate_queryset(products)
        if products and page is not None:
            return self.get_paginated_response(self.serializer_class(products, many=True).data)
        return Response('Not found', status=status.HTTP_404_NOT_FOUND)


class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )


class ProductDetailView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    serializer_class = ProductSerializer

    def get(self, request, slug, format=None):

        if Product.objects.filter(slug=slug).exists():
            product = Product.objects.get(slug=slug)

            related_products = product.category.products.filter(
                parent=None).order_by("?").exclude(id=product.id)

            if product.variants.all():
                products_colors = list(
                    product.variants.all().exclude(id=product.id))
            elif product.parent:
                products_colors = list(
                    product.parent.variants.all().exclude(id=product.id))
                related_products = list(product.category.products.filter(
                    parent=None).exclude(id=product.parent.id))

                products_colors.append(product.parent)
            else:
                products_colors = []

            Product.objects.filter(slug=slug).update(
                num_visits=product.num_visits + 1,
                last_visit=timezone.now(),
            )
            characteristic = []
            images = []
            if CharacteristicProduct.objects.filter(product=product).exists():
                characteristic = CharacteristicProduct.objects.filter(
                    product=product)
            if ProductImage.objects.filter(product=product).exists():
                images = ProductImage.objects.filter(product=product)

            characteristic = CharacteristicProductSerializer(
                characteristic, many=True)
            images = ProductImageSerializer(images, many=True)

            return Response({
                'characteristic': characteristic.data,
                'images': images.data,
                'related': self.serializer_class(related_products, many=True).data[:4],
                'colors': self.serializer_class(products_colors, many=True).data,
                'product': self.serializer_class(product).data,
            }, status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ProductsCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )

    def get(self, request, slug, format=None, *args, **kwargs):
        if Category.objects.filter(slug=slug).exists():
            category = Category.objects.get(slug=slug)
            if not category.parent:
                filtered_categories = Category.objects.filter(parent=category)
                products = Product.objects.filter(
                    category__in=filtered_categories)
            else:
                products = Product.objects.filter(
                    category=category)

            page = self.paginate_queryset(products)
            if products and page is not None:
                return self.get_paginated_response(self.serializer_class(products, many=True).data)
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'error': 'Category with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ListBySearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()
    def post(self, request, format=None, *args, **kwargs):
        data = self.request.data

        categories = data['categories']
        brands = data['brands']
        order = data['order']
        sort_by = data['sort_by']
        price_range = data['price_range']

        if len(categories) == 0:
            self.queryset = self.queryset
        else:
            filtered_categories = []
            for cat in categories:
                print(cat)
                filtered_categories.append(cat)
            print(self.queryset)

            self.queryset = self.queryset.filter(
                category__in=filtered_categories)
            print(self.queryset)

        if len(brands) == 0:
            self.queryset = self.queryset

        else:
            filtered_brands = []
            for brand in brands:
                filtered_brands.append(brand)
            self.queryset = self.queryset.filter(brand__in=filtered_brands)

        if not (sort_by == 'date_added' or sort_by == 'price' or sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_added'

        if order == 'desc':
            sort_by = '-' + sort_by
            self.queryset = self.queryset.order_by(sort_by)
        elif order == 'asc':
            self.queryset = self.queryset.order_by(sort_by)
        else:
            self.queryset = self.queryset.order_by(sort_by)

         # Filtrar por precio
        if price_range == '1 - 50':
            self.queryset = self.queryset.filter(price__gte=1)
            self.queryset = self.queryset.filter(price__lt=51)
        elif price_range == '51 - 70':
            self.queryset = self.queryset.filter(price__gte=51)
            self.queryset = self.queryset.filter(price__lt=71)
        elif price_range == '71 - 90':
            self.queryset = self.queryset.filter(price__gte=71)
            self.queryset = self.queryset.filter(price__lt=91)
        elif price_range == '91 - 119':
            self.queryset = self.queryset.filter(price__gte=91)
            self.queryset = self.queryset.filter(price__lt=120)
        elif price_range == 'Más de 120':
            self.queryset = self.queryset.filter(price__gte=120)

        # page = self.paginate_queryset(self.queryset)
        # print(page, "Page")
        # print(self.queryset, "products")
        # if page :
        #     return self.get_paginated_response(self.serializer_class(page, many=True).data)
        
        serializer = self.serializer_class(self.queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class GetSubCategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny, )
    queryset = Category.objects.all()

    def get(self, request, slug, format=None, *args, **kwargs):
        if Category.objects.filter(slug=slug).exists():
            self.queryset = self.queryset.get(slug=slug)
            return Response(self.serializer_class(self.queryset).data)
        else:
            return Response(
                {'error': 'Category with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)
