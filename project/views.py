from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from group.models import Group


class ProjectListCreateView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        project_name = data.get('name')
        if project_name:
            project = Project.objects.create(name=project_name)
            main_group = Group.objects.create(name=f"{project_name} Main Group", project=project)
            project.main_group = main_group
            project.save()
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Project name is required"}, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
