from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test


# Декоратор, который проверяет, что пользователь является менеджером
def manager_required(user):
    return user.is_authenticated and user.user_type == 'manager'
