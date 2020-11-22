from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "veyron_kolesa.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import veyron_kolesa.users.signals  # noqa F401
        except ImportError:
            pass
