from django.contrib.auth.models import AbstractUser
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
