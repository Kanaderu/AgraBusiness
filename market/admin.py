from django.contrib import admin
from .models import UserInfo, PaymentMethod, CreditCard, BankAccount
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'UserInfo'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PaymentMethodAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['billing_address_line1',
                           'billing_address_line2',
                           'billing_zip_code',
                           'billing_state',
                           'billing_city']}),
        ('Credit Card', {'fields': ['billing_credit_card']}),
        ('Bank Account', {'fields': ['billing_bank_account']})
    ]


admin.site.register(PaymentMethod, PaymentMethodAdmin)


class CreditCardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name',
                           'number',
                           'ccv',
                           'exp']})
    ]


admin.site.register(CreditCard, CreditCardAdmin)


class BankAccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['first_name',
                           'last_name',
                           'routing_number',
                           'account_number']})
    ]


admin.site.register(BankAccount, BankAccountAdmin)