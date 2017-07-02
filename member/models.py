from django.contrib.auth import base_user
from django.db import models


class MemberManager(base_user.BaseUserManager):
    def create_user(self, username, email, password=None):
        if (not username) or (not email):
            raise ValueError('Username dan eamil harus diisi')

        member = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        member.set_password(password)
        member.save(using=self.db)

        return member

    def create_superuser(self, username, email, password):
        member = self.create_user(
            username=username,
            email=email,
            password=password,
        )

        member.is_admin = True
        member.save(using=self.db)
        return member


class Member(base_user.AbstractBaseUser):
    username = models.CharField(
        max_length=25,
        editable=True,
        unique=True,
    )
    name = models.CharField(
        max_length=25,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    object = MemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split(' ')[0]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
