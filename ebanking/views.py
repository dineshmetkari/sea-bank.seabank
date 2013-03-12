import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, render_to_response, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.db.models import Sum

from ebanking.models import *
from ebanking.forms import *
from ebanking.sms import Sms
from ebanking.utils import random_string



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
def index(request):
    accounts = Account.objects.filter(user__username=request.user)
    for a in accounts:
        a.transactions = a.transaction_set.filter(confirmed=True).aggregate(Sum('value'))
        if a.transactions.get("value__sum") is not None:
            a.sum = 25000 - a.transactions.get("value__sum")
        else:
            a.sum = 25000
    return render(request,'ebanking/index.html', {'accounts': accounts})


@login_required
def history(request, account_id):
    a = Account.objects.get(pk=account_id)
    t = list(a.transaction_set.filter(confirmed=True).order_by('-pk'))
    return render(request,'ebanking/history.html', {'transactions': t})


@login_required
def transfer_form(request, account_id):

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            t = Transaction();
            t.sender_account = Account.objects.get(pk=account_id)
            t.recipient_account = request.POST['recipient_account']
            t.title = request.POST['title']
            t.recipient_name = request.POST['recipient_name']
            t.date = request.POST['date']
            t.value = request.POST['value']
            t.sms_code = random_string(4)

            request.session['transaction'] = t
            return HttpResponseRedirect('confirm.html')
    else:
        form = TransactionForm()

    return render(request, 'ebanking/transfer_form.html', {
        'form': form,
        'account_id': account_id
    })


@login_required
def transfer_confirm(request, account_id):

    t = request.session['transaction']

    if request.method == 'POST':
        if not t.sms_code == request.POST['sms_code']:
            return render_to_response('ebanking/transfer_confirm.html', 
                {'account_id': account_id, 'transaction': t, 'error_message': 'Kod SMS jest niepoprawny!'},
                 context_instance=RequestContext(request))

        t.confirmed = True
        t.save()
        return HttpResponseRedirect('success.html')
    else:
        now = datetime.datetime.now()
        smsMessage = "Kod dla operacji z dnia "+now.strftime("%d/%m/%Y")+", godziny "+now.strftime("%H:%M")+": " + t.sms_code
        sms = Sms(request.user.get_profile().telephone_number, smsMessage)
        sms.send()

        a = Account.objects.get(pk=account_id)
        a.transaction_set.add(t);
        a.save();
        t.save();

    return render_to_response('ebanking/transfer_confirm.html', 
        {'account_id': account_id, 'transaction': t}, context_instance=RequestContext(request))
