from django.urls import path

from .views import ListCategoryView,ListProductHomeView,ListBrandView,ListProductView

app_name = "product"

urlpatterns = [
    path('categories', ListCategoryView.as_view()),
    path('products_homepage', ListProductHomeView.as_view()),
    path('brands', ListBrandView.as_view()),
    path('products', ListProductView.as_view()),
]