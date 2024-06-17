from rest_framework import serializers
from users.serializers import UserSerializer
from group.models import Group


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    subgroups = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'parent_group', 'members', 'subgroups']

    def get_subgroups(self, obj):
        subgroups = obj.subgroups.all()
        serializer = self.__class__(subgroups, many=True)
        return serializer.data


class SubgroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'parent_group', 'members', 'subgroups']
