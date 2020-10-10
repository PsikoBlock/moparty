from mopidy_json_client import MopidyClient
from django.conf import settings

from . import models, serializers

backends_to_uris = {
    'local': 'local:',
    'spotify': 'spotify',
    'youtube': 'youtube:',
    'soundcloud': 'soundcloud:'
}

def start_client():
    global mopidy_client
    mopidy_client = MopidyClient(ws_url='ws://' + settings.MOPIDY_SERVER + '/mopidy/ws')
    # TODO bind events
    # mopidy_client.bind_event('track_playback_started', print_track_info)

def search_tracks(query, backends=backends_to_uris.keys()):
    from .mopidy_client import mopidy_client
    searchresult = {}
    uri_schemes = ['yt:' if backend == 'youtube' else f'{backend}:' for backend in backends]
    mopidy_results = mopidy_client.library.search(query={'any': [query]}, uris=uri_schemes)
    for backend in backends:
        for result in mopidy_results:
            print(result['uri'])
            if result['uri'].startswith(backends_to_uris[backend]):
                try:
                    tracklist = [models.Track.objects.parse_track_from_mopidy(track) for track in result['tracks']]
                except KeyError:
                    tracklist = []
                searchresult[backend] = serializers.TrackSerializer(tracklist, many=True, read_only=True).data
                break
    
    return searchresult
