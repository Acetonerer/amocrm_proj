from django.db import models


class User(models.Model):
    user_id = models.IntegerField(unique=False)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    group = models.ForeignKey('group.Group', related_name='members', on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # responsibilities = models.JSONField(default=list)

    def __str__(self):
        return self.name
