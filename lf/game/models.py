from django.db import models


class GameFile(models.Model):
    file = models.FileField(upload_to='game_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Gamer(models.Model):
    name = models.CharField(max_length=100)
    gamer_id = models.IntegerField()
    team_color = models.IntegerField()
    weapon_damage = models.IntegerField()
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
