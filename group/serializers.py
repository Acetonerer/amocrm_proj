from rest_framework import serializers
from users.serializers import UserSerializer
from group.models import Group


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    subgroups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'parent_group', 'members', 'subgroups', 'project']
