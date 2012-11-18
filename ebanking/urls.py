from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='ebanking/index.html')),
    url(r'^login/$', TemplateView.as_view(template_name='ebanking/login.html')),
)