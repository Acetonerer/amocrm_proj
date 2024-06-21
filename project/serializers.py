from rest_framework import serializers
from group.serializers import GroupSerializer
from users.serializers import UserSerializer
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    main_group = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['amo_id', 'name', 'main_group']

    def get_main_group(self, obj):
        main_group = obj.main_group
        if main_group:
            return self._serialize_group_with_subgroups(main_group)
        return None

    def _serialize_group_with_subgroups(self, group):
        group_data = GroupSerializer(group).data
        subgroups = group.subgroups.all()
        group_data['subgroups'] = [self._serialize_group_with_subgroups(subgroup) for subgroup in subgroups]
        return group_data
