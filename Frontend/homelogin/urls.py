from django.conf.urls import url
from .views import Home, Twitch

urlpatterns = [
    # Examples:
    # url(r'^$', 'Frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^settings/$', Home.as_view(), name='home'),
    url(r'twitch/$', Twitch.as_view(), name='twitch'),
]
