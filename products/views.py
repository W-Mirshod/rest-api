from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from products.models import Category


class IndexPage(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = [
            {'title': category.title,
             'slug': category.slug,
             'created_at': category.created_at,
             'updated_at': category.updated_at} for category in Category.objects.all()]

        return JsonResponse(data=categories, safe=False, status=status.HTTP_200_OK)
