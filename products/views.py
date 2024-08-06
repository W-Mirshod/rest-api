from rest_framework import status
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from products.models import Category
from products.serializers import CategorySerializer


class CategoryListPage(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class CategoryDetailPage(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'

# class CategoriesPage(APIView):
#     permission_classes = (AllowAny,),
#
#     def get(self, request):
#         categories = [
#             {'title': category.title,
#              'slug': category.slug,
#              'created_at': category.created_at,
#              'updated_at': category.updated_at} for category in Category.objects.all()]
#
#         return JsonResponse(data=categories, safe=False, status=status.HTTP_200_OK)


# class CategoryDetailPage(APIView):
#     permission_classes = (AllowAny,)
#
#     def get_object(self, slug):
#         return get_object_or_404(Category, slug=slug)
#
#     def get(self, request, slug):
#         category = self.get_object(slug)
#         serializer = CategorySerializer(category)
#         return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
