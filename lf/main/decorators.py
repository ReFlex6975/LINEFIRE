from django.core.exceptions import PermissionDenied


# Декоратор, который проверяет, что пользователь является менеджером
def manager_required(user):
    return user.is_authenticated and user.user_type == 'manager'


# Декоратор, который проверяет, что пользователь является администратором
def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return _wrapped_view
