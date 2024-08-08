from django.urls import path
from products.views.category import CategoryList, CategoryDetail
from products.views.group import GroupList

urlpatterns = [
    # category
    path('categories/', CategoryList.as_view()),
    path('categories/detail/<slug:category_slug>/', CategoryDetail.as_view()),

    # group
    path('categories/<slug:groups_slug>', GroupList.as_view())
]
