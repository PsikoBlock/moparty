from rest_framework import serializers

from . import models


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = ['uri', 'data', 'image']


class PlaylistDetailSerializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField()
    class Meta:
        model = models.Playlist
        fields = '__all__' 
    
    def get_tracks(self, instance):
        tracks = instance.tracks.all().order_by('position')
        return TrackSerializer(tracks, many=True, read_only=True).data


class PlaylistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ['id', 'playlist_of', 'wishlist_of']
