from django.db import models


class GameFile(models.Model):
    file = models.FileField(upload_to='game_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
