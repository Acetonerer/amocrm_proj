from rest_framework import serializers
from group.models import Group
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    subgroups = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'parent_group', 'members', 'subgroups', 'result']

    def get_subgroups(self, obj):
        subgroups = obj.subgroups.all()
        return GroupSerializer(subgroups, many=True).data


class SubgroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'parent_group', 'members', 'subgroups']
