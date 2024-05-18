from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    group = models.ForeignKey('group.Group', related_name='members', on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.name
