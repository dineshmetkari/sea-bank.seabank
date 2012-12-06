from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from ebanking.models import UserProfile, Account, Transaction, Property

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profil'

class AccountInline(admin.StackedInline):
    model = Account
    extra = 3

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, AccountInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.unregister(Site)

admin.site.register(Transaction)
admin.site.register(Property)
