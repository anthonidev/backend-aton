from django.urls import path

from .views import (ListBrandView, ListBySearchView, ListCategoryView,
                    ListProductHomeView, ListProductView, ProductDetailView)

app_name = "product"

urlpatterns = [
    path("categories", ListCategoryView.as_view()),
    path("products_homepage", ListProductHomeView.as_view()),
    path("brands", ListBrandView.as_view()),
    path("products", ListProductView.as_view()),
    path("filter", ListBySearchView.as_view()),
    path("<slug>", ProductDetailView.as_view()),
]
