
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


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
