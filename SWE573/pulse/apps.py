from django.apps import AppConfig
from SWE573.pulse.helpers import twitter_helper as tw


class PulseConfig(AppConfig):
    name = 'pulse'

    def ready(self):
        tw.initialize()
