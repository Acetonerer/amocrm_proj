from rest_framework import serializers
from group.serializers import GroupSerializer
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    main_group = GroupSerializer(read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'main_group', 'groups']
