from revproxy.views import ProxyView
from django.conf import settings

class MopidyPictureProxyView(ProxyView):
    upstream = 'http://' + settings.MOPIDY_SERVER + '/local'
