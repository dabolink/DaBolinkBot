from django.conf.urls import url
from .views import Home, Features, Contact, Twitch

urlpatterns = [
    # Examples:
    # url(r'^$', 'Frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', Home.as_view(), name='home'),
    url(r'features/$', Features.as_view(), name='features'),
    url(r'contact-us/$', Contact.as_view(), name='contact'),
    url(r'twitch/$', Twitch.as_view(), name='twitch'),
]