from django.apps import AppConfig


class PayrollsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "payrolls"

    def ready(self):
        import payrolls.signals
