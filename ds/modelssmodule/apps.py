from django.apps import AppConfig


class ModelssmoduleConfig(AppConfig):
    name = 'modelssmodule'

    def ready(self):
        import modelssmodule.signals.handlers
