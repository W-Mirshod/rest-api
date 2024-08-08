from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from products.models import Category
from products.serializers import CategorySerializer


class CategoryList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_slug):
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
