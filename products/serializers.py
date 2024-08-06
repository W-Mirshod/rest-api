from products.models import Category
from django.utils.text import slugify

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data.pop('title', '')
        slug = slugify(title)
        validated_data['title'] = slug
        return super().create(validated_data)
