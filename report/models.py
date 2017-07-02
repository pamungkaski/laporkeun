from django.db import models

from task import models as task_models
from member import models as member_models


class Report(models.Model):
    done = models.TextField(
        blank=False,
    )
    todo = models.TextField(
        blank=False,
    )
    problem = models.TextField(
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    task = models.ForeignKey(
        task_models.Task,
        on_delete=models.CASCADE
    )
    reporter = models.ForeignKey(
        member_models.Member,
        on_delete=models.CASCADE
    )
