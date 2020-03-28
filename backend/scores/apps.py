from django.apps import AppConfig


class ScoresConfig(AppConfig):
    name = 'scores'

    #to set the score app to listen to signals
    def ready(self):
        import scores.signals