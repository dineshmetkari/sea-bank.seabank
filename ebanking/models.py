from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	telephone_number = models.CharField("numer telefonu", max_length=15)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Account(models.Model):
	class Meta:
		verbose_name = "konto"
		verbose_name_plural = "konta"

	user = models.ForeignKey(User)
	iban = models.CharField("IBAN", max_length=200)
	currency = models.CharField("waluta", max_length=3)

class Transactions(models.Model):
	class Meta:
		verbose_name = "Operacja"
		verbose_name_plural = "Operacje"
	account = models.ForeignKey(Account)
	description = models.CharField("opis", max_length=200)
	date = models.DateField("data operacji")
	value = models.IntegerField("kwota operacji")
	smscode = models.CharField("kod sms", max_length=10)
	confirmed = models.BooleanField("potwierdzony")