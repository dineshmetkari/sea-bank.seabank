from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def login(request):
	if request.method != 'POST':
		return render_to_response('ebanking/login.html', context_instance=RequestContext(request))
	
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		auth_login(request, user)
		return HttpResponseRedirect(reverse('index'))
	else:
		return render_to_response('ebanking/login.html', {
			'error_message': "Invalid login or password.",
		}, context_instance=RequestContext(request))


def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse('logout_success'))