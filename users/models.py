from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, Group, Permission
from django.db import models
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь с таким email же существует')
        username = get_random_string(20)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.CharField(verbose_name='Адрес электронной почты', max_length=255, unique=True)
    # groups = models.ManyToManyField(Group, related_name="customuser_set")
    username = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        null=True
    )
    objects = CustomUserManager()
    status = models.BooleanField(
        default=False,
        verbose_name='Подтвержден/Не подтвержден'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))
        self.email = self.email

    @property
    def is_active(self):
        return self.is_superuser or self.status
