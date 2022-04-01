
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


class ListBrandView(generics.ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None

    def get(self, request, format=None, *args, **kwargs):
        queryset = Brand.objects.all()
        return Response({'brands': self.serializer_class(queryset, many=True).data}, status=status.HTTP_200_OK)


class ListCategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None, *args, **kwargs):
        category = Category.objects.all()
        page = self.paginate_queryset(category)
        if category and page is not None:
            return self.get_paginated_response(self.serializer_class(category, many=True).data)
        return Response('Not found', status=status.HTTP_404_NOT_FOUND)


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
                parent=None).exclude(id=product.id)

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
            characteristic=[]
            images=[]
            if CharacteristicProduct.objects.filter(product=product).exists():
                characteristic=CharacteristicProduct.objects.filter(product=product)
            if ProductImage.objects.filter(product=product).exists():
                images=ProductImage.objects.filter(product=product)
                
            characteristic=CharacteristicProductSerializer(characteristic,many=True)
            images=ProductImageSerializer(images,many=True)
            
            return Response({
                'characteristic': characteristic.data,
                'images': images.data,
                'related': self.serializer_class(related_products, many=True).data,
                'colors': self.serializer_class(products_colors, many=True).data,
                'product': self.serializer_class(product).data,
            }, status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)
