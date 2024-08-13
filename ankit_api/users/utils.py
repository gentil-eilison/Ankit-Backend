def user_directory_path(instance, filename):
    return f"users/{instance.user.id}/{filename}"


def set_history_user_null(historical_instance, user):
    if user:
        historical_instance.history_user = None
