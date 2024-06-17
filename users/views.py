from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from group.models import Group
from .models import User
from .serializers import UserSerializer


# class UserListCreateView(APIView):
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


class RemoveUserFromSubgroupView(APIView):
    def delete(self, request, user_id, group_id):
        try:
            # Потенциальная проверка на active, сравнение списка из пользователей из amocrm со списком пользователей в
            # проекте, если из пользователя нет в списке от amocrm,
            # но есть в проекте - этого пользователя из проекта удалить
            """
            Удаляем запись о пользователе по user_id и group_id
            """
            deleted_count, _ = User.objects.filter(user_id=user_id, group_id=group_id).delete()

            if deleted_count == 0:
                return Response({"error": "User not found in the specified group"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"success": True, "deletedUser": {"deletedUserId": user_id}}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
