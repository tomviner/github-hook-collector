from django.conf.urls import include, url
from django.contrib import admin
from collector.views import HookView

urlpatterns = [
    url(r'^hook/$', HookView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
