from django.urls import path
from products.views.group import GroupList, GroupDetail
from products.views.product import ProductList, ProductDetail, ProductAttribute, ProductsAttribute
from products.views.category import CategoryList, CategoryDetail

urlpatterns = [
    # category
    path('categories/', CategoryList.as_view()),
    path('categories/detail/<slug:category_slug>/', CategoryDetail.as_view()),

    # group
    path('categories/<slug:category_slug>/', GroupList.as_view()),
    path('categories/<slug:category_slug>/<slug:group_slug>/detail/', GroupDetail.as_view()),

    # product
    path('categories/<slug:category_slug>/<slug:group_slug>/', ProductList.as_view()),
    path('categories/<slug:category_slug>/<slug:group_slug>/<slug:product_slug>/', ProductDetail.as_view()),
    path('categories/<slug:category_slug>/<slug:group_slug>/<slug:product_slug>/attribute/', ProductAttribute.as_view()),
    path('categories/<slug:category_slug>/<slug:group_slug>/products/attributes/', ProductsAttribute.as_view()),
]
