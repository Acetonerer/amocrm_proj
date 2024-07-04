from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from project.models import Project
from .models import Group
from .serializers import GroupSerializer
from users.models import User
from users.serializers import UserSerializer
from django.middleware.csrf import get_token


class GroupListCreateView(APIView):

    def post(self, request):
        data = request.data
        amo_id = data.get('amo_id')
        group_name = data.get('name')
        parent_group_id = data.get('parent_group')

        if not amo_id or not group_name:
            return Response({"error": "amo_id and group name are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(amo_id=amo_id)

            # Если указан parent_group, проверяем его наличие
            parent_group = None
            if parent_group_id:
                parent_group = Group.objects.get(id=parent_group_id, project=project)

            # Создаем группу
            group = Group.objects.create(name=group_name, project=project, parent_group=parent_group)

            # Формируем ответ вручную
            response_data = {
                "id": group.id,
                "name": group.name,
                "amo_id": group.project.amo_id,
                "parent_group": group.parent_group.id if group.parent_group else None,
                "subgroups": [subgroup.id for subgroup in group.subgroups.all()],
                "members": []  # Assuming members field is required but empty as we're not handling it here
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response({"error": "Project with given amo_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({"error": "Parent group does not exist in the given project"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Обрабатываем возможные исключения и возвращаем ошибку сервера
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, group_id):
        csrf_token = get_token(request)
        print("CSRF Token:", csrf_token)  # Debugging: Check the CSRF token
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        new_itog = request.data.get('itog')
        if not new_itog:
            return Response({"error": "New result is required"}, status=status.HTTP_400_BAD_REQUEST)

        group.itog = new_itog
        group.save()

        return Response({"success": True, "updatedGroup": GroupSerializer(group).data}, status=status.HTTP_200_OK)


class GroupDetailView(APIView):

    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def delete(self, request, group_id):
        try:
            # Удаляем запись о пользователе по user_id и group_id
            deleted_count, _ = Group.objects.filter(id=group_id).delete()

            if deleted_count == 0:
                return Response({"error": "User not found in the specified group"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"success": True, "deletedGroup": {"deletedGroupId": group_id}}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        new_name = request.data.get('name')
        if not new_name:
            return Response({"error": "New name is required"}, status=status.HTTP_400_BAD_REQUEST)

        group.name = new_name
        group.save()

        return Response({"success": True, "updatedGroup": GroupSerializer(group).data}, status=status.HTTP_200_OK)


class GroupMembersView(APIView):
    def post(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['group'] = group_id  # Добавляем ID группы в данные запроса

        # Проверяем наличие пользователя в группе
        user_id = data.get('user_id')
        if user_id is not None and group.members.filter(user_id=user_id).exists():
            return Response({"error": "User already exists in the group"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, group_id, user_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = group.members.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found in this group"}, status=status.HTTP_404_NOT_FOUND)

        responsibilities = request.data.get('responsibilities')
        if responsibilities is None:
            return Response({"error": "Responsibilities are required"}, status=status.HTTP_400_BAD_REQUEST)

        user.responsibilities = responsibilities
        user.save()

        return Response({"success": True, "updated_user": UserSerializer(user).data}, status=status.HTTP_200_OK)


class GroupLeaderView(APIView):
    def put(self, request, group_id):
        leader_id = request.data.get('leader_id')
        if not leader_id:
            return Response({"error": "Leader ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        # Здесь используем filter вместо get, чтобы избежать MultipleObjectsReturned
        leaders = User.objects.filter(user_id=leader_id)
        if leaders.count() > 1:
            return Response({"error": "Multiple users found with the same user_id"}, status=status.HTTP_400_BAD_REQUEST)
        elif leaders.count() == 0:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        leader = leaders.first()

        if leader not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status=status.HTTP_400_BAD_REQUEST)

        leader.is_leader = True
        leader.save()

        return Response({'success': True, 'message': 'Leader assigned successfully.'}, status=status.HTTP_200_OK)
