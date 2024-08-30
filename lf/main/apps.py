from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Подключаем обработчик сигнала post_migrate
        post_migrate.connect(create_default_groups, sender=self)


# Обработчик сигнала для создания групп
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    # Пример создания групп
    managers_group, created = Group.objects.get_or_create(name='Менеджеры')
    players_group, created = Group.objects.get_or_create(name='Игроки')
    # Можно добавить права или другие настройки для групп
