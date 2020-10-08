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
