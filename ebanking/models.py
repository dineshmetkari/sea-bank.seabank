# -*- coding: utf-8 -*-

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

class Property(models.Model):
    class Meta:
        verbose_name = "właściwość"
        verbose_name_plural = "właściwości"
    name = models.CharField("nazwa", max_length=100)
    value = models.CharField("wartosc", max_length=100)
    def __unicode__(self):
        return self.name

class Account(models.Model):
    class Meta:
        verbose_name = "konto"
        verbose_name_plural = "konta"

    user = models.ForeignKey(User)
    iban = models.CharField("IBAN", max_length=30)
    currency = models.CharField("waluta", max_length=3)

class Transaction(models.Model):
    class Meta:
        verbose_name = "Operacja"
        verbose_name_plural = "Operacje"
    sender_account = models.ForeignKey(Account)
    recipient_account = models.CharField("rachunek odbiorcy", max_length=30)
    title = models.CharField("tytul przelewu", max_length=200)
    recipient_name = models.CharField("nazwa odbiorcy", max_length=40)
    date = models.DateField("data operacji")
    value = models.IntegerField("kwota operacji")
    sms_code = models.CharField("kod sms", max_length=10)
    confirmed = models.BooleanField("potwierdzony")
