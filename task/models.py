from django.db import models

from member import models as member_models
from project import models as project_models


class Task(models.Model):
    name = models.CharField(
        max_length=25,
        blank=False,
    )
    description = models.TextField(
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    project = models.ForeignKey(
        project_models.Project,
        on_delete=models.CASCADE,
    )
    assigned = models.ManyToManyField(
        member_models.Member,
        related_name='task_assigned',
    )
