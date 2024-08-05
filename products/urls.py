from django.urls import path

from products.views import IndexPage

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
]
