from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('homelogin.urls')),
    url(r'^home/', include('homelogin.urls')),
    url(r'^settings/', include('homelogin.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
