from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)
    avatar = models.ImageField(verbose_name='photo de profil', upload_to='avatars')
    bio = models.TextField(verbose_name='bio', blank=True)
    email = models.EmailField(verbose_name='adresse e-mail', blank=True)
    phone_number = models.CharField(verbose_name='numéro de téléphone', max_length=20, blank=True)
    birth_date = models.DateField(verbose_name='date de naissance', null=True, blank=True)
    social_media = models.URLField(verbose_name='réseaux sociaux', blank=True)
    location = models.CharField(verbose_name='localisation', max_length=255, blank=True)

    def __str__(self):
        return f'{self.username} : {" | ".join([role.name for role in self.roles.all()])}'
