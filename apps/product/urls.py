from django.urls import path

from .views import ListCategoryView,ListProductHomeView

app_name = "product"

urlpatterns = [
    path('categories', ListCategoryView.as_view()),
    path('products_homepage', ListProductHomeView.as_view()),
]