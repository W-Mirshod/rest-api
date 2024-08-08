from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Group
from products.serializers import GroupSerializer


class GroupList(APIView):
    def get(self, request, groups_slug):
        groups = Group.objects.filter(category__slug=groups_slug)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
