from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse
from django.conf import settings


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('manager', 'Manager'),
        ('player', 'Player'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def is_manager(self):
        return self.user_type == 'manager'

    def is_player(self):
        return self.user_type == 'player'


# ----------------------------------------------------------------------------------

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


# ----------------------------------------------------------------------------------

class Scenario(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    image = models.ImageField(upload_to='scenarios/', blank=True, null=True)

    def __str__(self):
        return self.title


# ----------------------------------------------------------------------------------

class Section(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.title


# ----------------------------------------------------------------------------------


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Удаляем старые изображения, если заменяем их новыми
        if self.pk:
            old = Equipment.objects.get(pk=self.pk)
            for field in ['image1', 'image2', 'image3', 'image4', 'image5']:
                old_image = getattr(old, field)
                new_image = getattr(self, field)
                if old_image != new_image:
                    if old_image and old_image != 'None' and default_storage.exists(old_image.path):
                        default_storage.delete(old_image.path)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем изображения при удалении объекта
        for field in ['image1', 'image2', 'image3', 'image4', 'image5']:
            image = getattr(self, field)
            if image and image != 'None' and default_storage.exists(image.path):
                default_storage.delete(image.path)
        super().delete(*args, **kwargs)


class Gamer(models.Model):
    name = models.CharField(max_length=100)
    gamer_id = models.IntegerField()
    team_color = models.IntegerField()
    wiapon_damage = models.IntegerField()
    tager_type = models.IntegerField()
    fire_count = models.IntegerField()
    frags = models.IntegerField()
    killed = models.IntegerField()
    medicine = models.IntegerField()
    ammo = models.IntegerField()
    damage = models.IntegerField()
    game_time = models.DurationField()

    def __str__(self):
        return self.name
