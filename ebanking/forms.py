from django.forms import ModelForm

from ebanking.models import *

class TransactionForm(ModelForm):
   class Meta:
         model = Transaction
         exclude = ('sender_account','sms_code','confirmed')
