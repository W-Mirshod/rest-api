from products.models import Category
from django.utils.text import slugify
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Category
        fields = '__all__'
