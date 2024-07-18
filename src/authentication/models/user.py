from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db import models

from base.models import LogMixin


class CustomUserManager(UserManager):
    def _create_user(self, email, name, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email=None, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, LogMixin):
    name = models.CharField('nome', max_length=60, null=True, blank=False)
    email = models.EmailField('e-mail', unique=True, max_length=320)
    phone = models.CharField('telefone', max_length=20, unique=True, null=True, blank=True)

    is_staff = models.BooleanField('usuário interno', default=False,
                                   help_text='Indica que o usuário consegue acessar a área administrativa.')
    is_active = models.BooleanField('é ativo', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'usuário'

    def __str__(self):
        return f'{self.name} - {self.email}' if self.name else self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.email = self.email.lower()

    def get_full_name(self):
        return self.name

    @property
    def first_name(self) -> str:
        first_name = self.name.split()[0].title() if self.name is not None else None
        return first_name

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
