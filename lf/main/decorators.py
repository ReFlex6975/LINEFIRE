
# Декоратор, который проверяет, что пользователь является менеджером
def manager_required(user):
    return user.is_authenticated and user.user_type == 'manager'
