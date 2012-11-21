from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='ebanking/')),
	url(r'^ebanking/', include('ebanking.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
