from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from products.serializers import ProductSerializer, ProductDetailSerializer, AttributeSerializer, LoginSerializer, \
    RegisterSerializer
from root.permissions import CustomPermissions


class ProductList(APIView):
    # @method_decorator(cache_page(60 * 5))
    def get(self, request, category_slug, group_slug):
        cache_key = f'product_list_{category_slug}_{group_slug}'
        product_data = cache.get(cache_key)

        if not product_data:
            products = Product.objects.select_related('group__category').filter(
                group__category__slug=category_slug,
                group__slug=group_slug
            )
            serializer = ProductSerializer(products, many=True, context={'request': request})
            product_data = serializer.data
            cache.set(cache_key, product_data, 900)
        return Response(product_data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    permission_classes = (CustomPermissions,)

    def get(self, request, category_slug, group_slug, product_slug):
        cache_key = f'product_detail_{product_slug}'
        product_data = cache.get(cache_key)

        if not product_data:
            product = get_object_or_404(Product, slug=product_slug)
            serializer = ProductDetailSerializer(product)
            product_data = serializer.data
            cache.set(cache_key, product_data, 900)

        return Response(product_data, status=status.HTTP_200_OK)

    def post(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = ProductDetailSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_slug, group_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, category_slug, group_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsAttribute(APIView):
    def get(self, request, category_slug, group_slug):
        products = Product.objects.select_related('group__category').filter(
            group__category__slug=category_slug,
            group__slug=group_slug
        )
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


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "about": "Not Exist"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "user": RegisterSerializer(user).data,
                "token": token.key,
                "message": "User created successfully."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
