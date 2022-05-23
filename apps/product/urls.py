from django.urls import path

from .views import GetSubCategoryView, ListCategoryView,ListProductHomeView,ListBrandView,ListProductView, ProductDetailView,ListBySearchView,ProductsCategory

app_name = "product"

urlpatterns = [
    path('categories', ListCategoryView.as_view()),
    path('products_homepage', ListProductHomeView.as_view()),
    path('brands', ListBrandView.as_view()),
    path('products', ListProductView.as_view()),
    path('filter', ListBySearchView.as_view()),
    path('<slug>', ProductDetailView.as_view()),
    path('category/<slug>', ProductsCategory.as_view()),
    path('category/subcategory/<slug>', GetSubCategoryView.as_view()),
]