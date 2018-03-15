from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class CreditCard(models.Model):
    name = models.CharField(max_length=256, help_text="Name on Credit Card")
    number = models.IntegerField(help_text="Credit Card Number")  # normally a 12 digit integer
    ccv = models.IntegerField(help_text="Credit Card CCV (Card Verification Value)")  # normally a 3 or 4 digit integer
    exp = models.DateField()

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    first_name = models.CharField(max_length=256, help_text="First Name Associated with Bank Account")
    last_name = models.CharField(max_length=256, help_text="Last Name Associated with Bank Account")
    routing_number = models.IntegerField(help_text="Bank Account Routing Number")  # normally a 9 digit integer
    account_number = models.IntegerField(help_text="Bank Account Account Number")  # normally a 17 digit integer

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class PaymentMethod(models.Model):
    billing_address_line1 = models.CharField(max_length=256, help_text="Billing Address Line 1")
    billing_address_line2 = models.CharField(max_length=256, help_text="Billing Address Line 2", blank=True)
    billing_zip_code = models.IntegerField(default=0, help_text="Billing Address Zip Code")
    billing_state = models.CharField(max_length=2, help_text="Billing Address State")
    billing_city = models.CharField(max_length=256, help_text="Billing Address City")
    billing_credit_card = models.ForeignKey('CreditCard', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    billing_bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return self.billing_address_line1

    def save(self, *args, **kwargs):
        self.billing_state = self.billing_state.upper()
        return super(PaymentMethod, self).save(*args, **kwargs)

class UserInfo(models.Model):
    USER_TYPE = (
        ('f', 'Farmer'),
        ('c', 'Customer'),
        ('m', 'Manager')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=USER_TYPE, default='c', help_text="User Account Type")
    payment_method = models.OneToOneField(PaymentMethod, default=None, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        pMethod = PaymentMethod.objects.create()
        UserInfo.objects.create(user=instance, payment_method=pMethod)


@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()
