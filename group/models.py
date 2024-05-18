from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    parent_group = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subgroups')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.name
