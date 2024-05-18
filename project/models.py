from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    main_group = models.OneToOneField('group.Group', on_delete=models.CASCADE, related_name='main_group_of_project')

    def __str__(self):
        return self.name
