from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# User Account Models
class UserInfo(models.Model):
    USER_TYPE = (
        ('f', 'Farmer'),
        ('c', 'Customer'),
        ('m', 'Manager')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, blank=True, null=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE, default='c', help_text="User Account Type")
    payment_method = models.OneToOneField('PaymentMethod', default=None, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    # auto create associated models when creating userinfo
    if created:
        pMethod = PaymentMethod.objects.create()
        cart = Cart.objects.create()
        UserInfo.objects.create(user=instance, payment_method=pMethod, cart=cart)


@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()


# Billing Models
class PaymentMethod(models.Model):
    billing_address_line1 = models.CharField(max_length=256, help_text="Billing Address Line 1")
    billing_address_line2 = models.CharField(max_length=256, help_text="Billing Address Line 2", blank=True)
    billing_zip_code = models.PositiveIntegerField(default=0, help_text="Billing Address Zip Code")
    billing_state = models.CharField(max_length=2, help_text="Billing Address State")
    billing_city = models.CharField(max_length=256, help_text="Billing Address City")

    def __str__(self):
        return self.billing_address_line1

    def save(self, *args, **kwargs):
        self.billing_state = self.billing_state.upper()
        return super(PaymentMethod, self).save(*args, **kwargs)


class CreditCard(models.Model):
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=256, help_text="Name on Credit Card")
    number = models.PositiveIntegerField(help_text="Credit Card Number")  # normally a 12 digit integer
    ccv = models.PositiveIntegerField(help_text="Credit Card CCV (Card Verification Value)")  # normally a 3 or 4 digit integer
    exp = models.DateField()

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    first_name = models.CharField(max_length=256, help_text="First Name Associated with Bank Account")
    last_name = models.CharField(max_length=256, help_text="Last Name Associated with Bank Account")
    routing_number = models.PositiveIntegerField(help_text="Bank Account Routing Number")  # normally a 9 digit integer
    account_number = models.PositiveIntegerField(help_text="Bank Account Account Number")  # normally a 17 digit integer

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Cart Models
class Cart(models.Model):
    subtotal = models.DecimalField(default=0.00, max_digits=25, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=25, decimal_places=2)

    def __str__(self):
        return self.subtotal + ' ' + self.total


class CartItem(models.Model):
    #produce_id = models.PositiveIntegerField()
    #produce_id = models.ForeignKey('ProduceItem', on_delete=models.CASCADE, to_field='produce_id')
    #produce_id = models.ForeignKey('ProduceItem', on_delete=models.CASCADE, to_field='id')
    cart = models.ForeignKey('Cart', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(default=0.00, max_digits=25, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=25, decimal_places=2)

    def __str__(self):
        return self.unit_cost + ' ' + self.quantity + ' ' + self.subtotal


# Inventory Produce
class ProduceItem(models.Model):
    #produce_id = models.PositiveIntegerField(unique=True)
    #produce_id = models.AutoField(primary_key=True)
    produce_name = models.CharField(max_length=256)
    #produce_type
    expiration = models.DateField()
    description = models.CharField(max_length=5000)
    price = models.DecimalField(default=0.00, max_digits=25, decimal_places=2)
    #image_name
    supplier = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + self.produce_name + ' ' + self.description + ' ' + str(self.price)


class ProduceGroup(models.Model):
    #produce_type
    inventory_pool = models.ForeignKey('InventoryPool', on_delete=models.CASCADE)
    group_description = models.CharField(max_length=5000)
    in_stock_quantity = models.PositiveIntegerField()


class InventoryPool(models.Model):
    total_stock_quantity = models.PositiveIntegerField()