from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='/mail/')),
	url(r'^mail/', include('mail.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
	
)
