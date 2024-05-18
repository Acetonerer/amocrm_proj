from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group
from .serializers import GroupSerializer
from users.models import User
from users.serializers import UserSerializer


class GroupListCreateView(APIView):
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):

    def get(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GroupSerializer(group)
        return Response(serializer.data)


class GroupMembersView(APIView):
    def post(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(group=group)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupLeaderView(APIView):
    def put(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        leader_id = request.data.get('leader_id')
        try:
            leader = User.objects.get(id=leader_id, group=group)
            leader.is_leader = True
            leader.save()
            return Response({'success': True, 'message': 'Leader assigned successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found in this group'}, status=status.HTTP_404_NOT_FOUND)
