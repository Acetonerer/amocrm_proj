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
        main_group_serializer = GroupSerializer(main_group)
        other_groups = obj.groups.exclude(id=main_group.id)
        other_groups_serializer = GroupSerializer(other_groups.filter(parent_group=None), many=True)

        members = []
        subgroups = []
        for group in other_groups:
            if group.parent_group_id == main_group.id:
                subgroups.append(group)
            members.extend(group.members.all())

        members_serializer = UserSerializer(members, many=True)
        main_group_data = main_group_serializer.data
        main_group_data['members'] = members_serializer.data
        main_group_data['subgroups'] = other_groups_serializer.data
        return main_group_data
