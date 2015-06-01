from django.conf.urls import url
from .views import Home, Twitch

urlpatterns = [
    # Examples:
    # url(r'^$', 'Frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^$', Home.as_view(), name='home'),
    url(r'twitch/$', Twitch.as_view(), name='twitch'),
]