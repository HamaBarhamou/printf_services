from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)
    avatar = models.ImageField(verbose_name='photo de profil', upload_to='avatars')

    def __str__(self):
        return f'{self.username} : {" | ".join([role.name for role in self.roles.all()])}'
