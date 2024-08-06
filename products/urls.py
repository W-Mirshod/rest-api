from django.urls import path
from products.views import CategoryListPage, CategoryDetailPage

urlpatterns = [
    path('categories/', CategoryListPage.as_view(), name='category'),
    path('categories/detail/<slug:slug>/', CategoryDetailPage.as_view(), name='category_detail'),
]
