from django.apps import AppConfig


class JukeboxConfig(AppConfig):
    name = 'jukebox'
    verbose_name = 'Moparty Jukebox'
    
    def ready(self):
        from . import mopidy_client
        mopidy_client.start_client()
