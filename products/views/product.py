from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from products.serializers import ProductSerializer, ProductDetailSerializer, AttributeSerializer, LoginSerializer, \
    RegisterSerializer


class ProductList(APIView):
    def get(self, request, category_slug, group_slug):
        products = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    def get(self, request, category_slug, group_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
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


class ProductsAttribute(APIView):
    def get(self, request, category_slug, group_slug):
        products = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        serializer = AttributeSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductAttribute(APIView):

    def get(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = AttributeSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = AttributeSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(f"User: {user.username}, Token: {token.key}")

        response_data = {
            'success': True,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }

        return Response(response_data, status=status.HTTP_200_OK)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": RegisterSerializer(user).data,
                "message": "User created successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
