from django.urls import path
from products.views.category import CategoryList, CategoryDetail

urlpatterns = [
    # category
    path('categories/', CategoryList.as_view()),
    path('categories/detail/<slug:category_slug>/', CategoryDetail.as_view()),
]
