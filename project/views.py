from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from group.models import Group


class ProjectListCreateView(APIView):

    def post(self, request):
        data = request.data
        project_name = data.get('name')
        amo_id = data.get('amo_id')

        if not project_name or not amo_id:
            return Response({"error": "Project name and amo_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Создаем проект с указанным именем и amo_id
            project = Project.objects.create(name=project_name, amo_id=amo_id)
            # Создаем основную группу для проекта
            main_group = Group.objects.create(name=f"{project_name} Main Group", project=project)
            # Присваиваем основную группу проекту и сохраняем
            project.main_group = main_group
            project.save()

            # Формируем ответ вручную
            response_data = {
                "name": project.name,
                "amo_id": project.amo_id,
                "main_group": {
                    "id": main_group.id,
                    "name": main_group.name,
                    "amo_id": project.amo_id
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Обрабатываем возможные исключения и возвращаем ошибку сервера
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDetailView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)

            # Удаляем все группы, подгруппы и членов, связанные с проектом
            groups = Group.objects.filter(project=project)
            for group in groups:
                group.members.all().delete()  # Удаляем всех членов группы
                group.subgroups.all().delete()  # Удаляем все подгруппы
            groups.delete()  # Удаляем все группы

            return Response({"success": True, "message": "Project and all related data have been deleted."},
                            status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
