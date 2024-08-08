from rest_framework import status
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from products.serializers import ProductSerializer, ProductDetailSerializer


class ProductList(APIView):
    def get(self, request, category_slug, group_slug):
        products = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    def get(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
