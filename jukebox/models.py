from django.db import models
from django.contrib.auth.models import User


class Playlist(models.Model):
    pass

class TrackManager(models.Manager):
    def lookup_track_from_mopidy(self, uri, playlist, position):
        pass
        #uri
        #return parse_track_from_mopidy(track)
    
    def parse_track_from_mopidy(self, mopidy_track, playlist=None, position=None):
        uri = mopidy_track['uri']
        from .mopidy_client import mopidy_client
        try:
            image = mopidy_client.library.get_images([uri])[uri][0]['uri']
        except IndexError:
            image = None
        track = self.model(uri=uri, data=mopidy_track, image=image, playlist=playlist, position=position)
        return track


class Track(models.Model):
    uri = models.CharField(max_length=255, primary_key=True)
    data = models.JSONField()
    image = models.URLField(blank=True, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks', blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)
    
    objects = TrackManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['playlist', 'position'], name='unique_playlist_and_position'),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    wishlist = models.OneToOneField(Playlist, on_delete=models.SET_NULL, related_name='wishlist_of', null=True)
    wishlist_position = models.PositiveIntegerField(null=True)
    playlist = models.OneToOneField(Playlist, on_delete=models.SET_NULL, related_name='playlist_of', null=True)
