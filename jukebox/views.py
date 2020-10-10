from rest_framework import authentication, permissions, status, views, viewsets
from rest_framework.response import Response

from . import serializers
from . import models
from . import mopidy_client


class Search(views.APIView):
    """
    View to search for songs.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        """
        Search for songs
        """
        try:
            searchquery = self.request.GET['searchquery']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        backends = self.request.GET.getlist('backend', mopidy_client.backends_to_uris.keys())
        searchresult = mopidy_client.search_tracks(searchquery, backends)
        return Response(searchresult)


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    View playlists
    '''
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = models.Playlist.objects.all()

    def list(self, request):
        serializer = PlaylistListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def serialize_detail(playlist):
        serializer = PlaylistDetailSerializer(playlist)
        return Response(serializer.playlist)

    def retrieve(self, request, pk=None):
        playlist = get_object_or_404(self.queryset, pk=pk)
        return serialize_detail(playlist)


class UserPlaylistViewSet(PlaylistViewSet):
    '''
    View user playlists and modify own
    '''
    
    queryset = models.Playlist.objects.filter(playlist_of__isnull=False)
    
    def my(self, request):
        playlist = get_object_or_404(self.queryset.filter(playlist_of=request.user))
        return serialize_detail(playlist)


class UserWishlistViewSet(PlaylistViewSet):
    '''
    View user wishlists and modify own
    '''
    
    queryset = models.Playlist.objects.filter(wishlist_of__isnull=False)
    
    def my(self, request):
        playlist = get_object_or_404(self.queryset.filter(wishlist_of=request.user))
        return serialize_detail(playlist)
