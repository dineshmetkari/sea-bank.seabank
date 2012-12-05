from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='index.html'),name='index'),
	url(r'^login/$', 'ebanking.views.login',name='login'),
	url(r'^logout/$', 'ebanking.views.logout',name='loguot'),
	url(r'^logout/success.html$', TemplateView.as_view(template_name='ebanking/logout_success.html'),name='logout_success'),    
	url(r'^index.html$', login_required(
			TemplateView.as_view(template_name='ebanking/index.html'),
			redirect_field_name=''
		)),
	url(r'^(?P<account_id>\d+)/history/$', 'ebanking.views.history',name='history'),
	url(r'^(?P<account_id>\d+)/transfer/form.html$', 'ebanking.views.transfer_form',name='transfer_form'),
	url(r'^(?P<account_id>\d+)/transfer/confirm.html$', 'ebanking.views.transfer_confirm',name='transfer_confirm'),
	url(r'^(?P<account_id>\d+)/transfer/process.html$', 'ebanking.views.transfer_process',name='transfer_process'),
	url(r'^(?P<account_id>\d+)/transfer/success.html$', login_required(
			TemplateView.as_view(template_name='ebanking/transfer_success.html'),
			redirect_field_name=''
		)),
)
