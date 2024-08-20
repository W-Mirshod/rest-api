from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Group
from products.serializers import GroupSerializer


class GroupList(APIView):
    def get(self, request, category_slug):
        groups = Group.objects.select_related('category').filter(category__slug=category_slug)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug):
        groups = Group.objects.select_related('category').filter(category__slug=category_slug)
        groups.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupDetail(APIView):
    def get(self, request, category_slug, group_slug):
        groups = Group.objects.select_related('category').filter(
            category__slug=category_slug,
            slug=group_slug
        )
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request, category_slug, group_slug):
        groups = Group.objects.select_related('category').filter(
            category__slug=category_slug,
            slug=group_slug
        )
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug, group_slug):
        groups = Group.objects.select_related('category').filter(
            category__slug=category_slug,
            slug=group_slug
        )
        groups.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
