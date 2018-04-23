from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define User Admin
class UserInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'UserInfo'
    fieldsets = [
        (None, {'fields': ['user_type']})
    ]


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Define PaymentMethod Admin
class PaymentMethodAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('billing_address_line1',
                    'billing_address_line2',
                    'billing_zip_code',
                    'billing_state',
                    'billing_city')

    # editable fields
    fieldsets = [
        (None, {'fields': ['billing_address_line1',
                           'billing_address_line2',
                           'billing_zip_code',
                           'billing_state',
                           'billing_city']}),
    ]


admin.site.register(PaymentMethod, PaymentMethodAdmin)


# Define CreditCard Admin
class CreditCardAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('payment_method',
                    'name',
                    'number',
                    'ccv',
                    'exp')

    # editable fields
    fieldsets = [
        (None, {'fields': ['payment_method',
                           'name',
                           'number',
                           'ccv',
                           'exp']})
    ]


admin.site.register(CreditCard, CreditCardAdmin)


# Define BankAccount Admin
class BankAccountAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('first_name',
                    'last_name',
                    'routing_number',
                    'account_number')

    # editable fields
    fieldsets = [
        (None, {'fields': ['first_name',
                           'last_name',
                           'routing_number',
                           'account_number']})
    ]


admin.site.register(BankAccount, BankAccountAdmin)


# Define ProduceItem Admin
class ProduceItemAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('id',
                    'produce_name',
                    'expiration',
                    'description',
                    'price',
                    'supplier')

    # editable fields
    fieldsets = [
        (None, {'fields': ['produce_name',
                           'expiration',
                           'description',
                           'price',
                           'supplier']})
    ]


admin.site.register(ProduceItem, ProduceItemAdmin)


# Define Cart Admin
class CartAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('subtotal',
                    'total',
                    'user',)

    # editable fields
    fieldsets = [
        (None, {'fields': ['subtotal',
                           'total',
                           'user',]})
    ]


admin.site.register(Cart, CartAdmin)


# Define CartItem Admin
class CartItemAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('produce_item',
                    'cart',
                    'quantity',
                    'unit_cost',
                    'subtotal')

    # editable fields
    fieldsets = [
        (None, {'fields': ['produce_item',
                           'cart',
                           'quantity',
                           'unit_cost',
                           'subtotal']})
    ]


admin.site.register(CartItem, CartItemAdmin)


# Define ShippingInformation Admin
class ShippingInformationAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('shipping_address_line1',
                    'shipping_address_line2',
                    'shipping_zip_code',
                    'shipping_state',
                    'shipping_city',
                    #'shipping_cost'
                    )

    # editable fields
    fieldsets = [
        (None, {'fields': ['shipping_address_line1',
                           'shipping_address_line2',
                           'shipping_zip_code',
                           'shipping_state',
                           'shipping_city',
                           #'shipping_cost',
                           ]}),
    ]


admin.site.register(ShippingInformation, ShippingInformationAdmin)


# Define Order Admin
class OrderAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('user',
                    'date_created',
                    'date_last_modified',
                    'shipping_info',
                    'order_type',
                    'tax',
                    'tax_rate',
                    'subtotal',
                    'total',)

    # list read only fields on editable fields
    readonly_fields = ['date_created']

    # editable fields
    fieldsets = [
        (None, {'fields': ('user',
                           'date_created',
                           'date_last_modified',
                           'shipping_info',
                           'order_type',
                           'tax',
                           'tax_rate',
                           'subtotal',
                           'total')})
    ]


admin.site.register(Order, OrderAdmin)


# Define OrderItem Admin
class OrderItemAdmin(admin.ModelAdmin):
    # elements to show on list
    list_display = ('order',
                    'id',
                    'produce_name',
                    'expiration',
                    'description',
                    'supplier',
                    'unit_cost',
                    'quantity',
                    'subtotal')

    # editable fields
    fieldsets = [
        (None, {'fields': ['order',
                           'produce_name',
                           'expiration',
                           'description',
                           'supplier',
                           'unit_cost',
                           'quantity',
                           'subtotal']})
    ]


admin.site.register(OrderItem, OrderItemAdmin)
