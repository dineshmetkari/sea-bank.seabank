from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, render_to_response, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from ebanking.models import *
from ebanking.forms import *

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
            'error_message': "Niepoprawny login lub haslo!",
        }, context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('logout_success'))

@login_required
def history(request, account_id):
    a = Account.objects.get(pk=account_id)
    t = list(a.transaction_set.filter(confirmed=True))
    #if not t:
    #    raise Http404
    return render_to_response('ebanking/history.html', {'transactions': t})


@login_required
def transfer_form(request, account_id):

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # ...
            return HttpResponseRedirect('transfer_confirm')
    else:
        form = TransactionForm()
        return render(request, 'ebanking/transfer_form.html', {
            'form': form,
            'account_id': account_id
        })


@login_required
def transfer_confirm(request, account_id):
    t = Transaction();
    t.recipient_account = request.POST['recipient_account']
    t.title = request.POST['title']
    t.recipient_name = request.POST['recipient_name']
    t.date = request.POST['date']
    t.value = request.POST['value']
    t.sms_code = "CODE4U"
    a = Account.objects.get(pk=account_id)
    a.transaction_set.add(t);
    a.save();
    t.save();
    return render_to_response('ebanking/transfer_confirm.html', 
        {'account_id': account_id, 'transaction': t}, context_instance=RequestContext(request))

@login_required
def transfer_process(request, account_id):
    t = Transaction.objects.get(pk=request.POST['transaction'])
    if not t.sms_code == request.POST['sms_code']:
        raise Http404

    t.confirmed = True
    t.save()
    return HttpResponseRedirect('success.html')
