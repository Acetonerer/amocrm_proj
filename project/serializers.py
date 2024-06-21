from rest_framework import serializers
from group.serializers import GroupSerializer
from users.serializers import UserSerializer
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    main_group = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['amo_id', 'name', 'main_group', 'groups']

    def get_main_group(self, obj):
        main_group = obj.main_group
        if main_group:
            main_group_serializer = GroupSerializer(main_group)
            return main_group_serializer.data
        return None

    def get_groups(self, obj):
        main_group = obj.main_group
        all_groups = obj.groups.all()

        def get_subgroups(group):
            subgroups = group.subgroups.all()
            return GroupSerializer(subgroups, many=True).data

        project_groups = []
        for group in all_groups:
            if group.parent_group == main_group:
                group_data = GroupSerializer(group).data
                group_data['subgroups'] = get_subgroups(group)
                project_groups.append(group_data)

        return project_groups
