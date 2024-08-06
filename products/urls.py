from django.urls import path
from products.views import CategoriesPage, CategoryDetailPage, UpdateCategoryPage

urlpatterns = [
    path('categories/', CategoriesPage.as_view(), name='category'),
    path('categories/detail/<slug:slug>/', CategoryDetailPage.as_view(), name='category_detail'),
    path('categories/update/<slug:slug>/', UpdateCategoryPage.as_view(), name='category_update'),
]
