from django.db import models
from project.models import Project


class Group(models.Model):
    name = models.CharField(max_length=100, default='')
    parent_group = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subgroups')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='groups')
    itog = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name
