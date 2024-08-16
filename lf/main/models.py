from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.
class Buyer(AbstractUser):
    fio = models.CharField(max_length=30, unique=False)  # Полное имя
    dob = models.DateField(null=True, blank=True)  # Дата рождения

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='buyer_set',  # Измените related_name для предотвращения конфликта
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='buyer_set',  # Измените related_name для предотвращения конфликта
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Polygon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image1 = models.ImageField(upload_to='polygons/')
    image2 = models.ImageField(upload_to='polygons/', blank=True, null=True)
    image3 = models.ImageField(upload_to='polygons/', blank=True, null=True)
    image4 = models.ImageField(upload_to='polygons/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('polygon-list', kwargs={'pk': self.pk})

    # @receiver(post_migrate)
    # def create_groups(sender, **kwargs):
    #     if sender.name == 'main':  # Укажите имя вашего приложения
    #         # Создание групп
    #         user_group, created = Group.objects.get_or_create(name='User')
    #         manager_group, created = Group.objects.get_or_create(name='Manager')
    #         admin_group, created = Group.objects.get_or_create(name='Administrator')
    #
    #         # Пример создания разрешений
    #         # Обратите внимание: Вам нужно создать соответствующие разрешения
    #         # Если разрешения ещё не созданы, вы можете их создать и назначить здесь
