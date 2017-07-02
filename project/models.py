from django.db import models

from member import models as member_models


class Project(models.Model):
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

    admin = models.ManyToManyField(
        member_models.Member,
        related_name='project_admin'
    )

    member = models.ManyToManyField(
        member_models.Member,
        related_name='project_member'
    )
