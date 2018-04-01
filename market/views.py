from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import DetailView, FormView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from decimal import Decimal
from django.http import HttpResponse


# function that updates a cart's details with its associated cart items
def UpdateCartDetails(cart):
    # get items in user's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # compute cart subtotal
    sum = Decimal(0.00)

    for cart_item in cart_items:
        sum += cart_item.unit_cost * cart_item.quantity

    # update cart
    cart = cart
    cart.subtotal = sum
    cart.tax = cart.subtotal * cart.tax_rate / Decimal(100.00)
    cart.total = cart.tax + cart.subtotal
    cart.save()


# Edit User View
class EditUserView(View):
    user_form = DjangoUserForm
    userinfo_form = UserInfoForm
    pmethod_form = PaymentMethodForm
    template_name = 'user.html'

    decorators = [transaction.atomic, login_required]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        user_form = self.user_form(instance=request.user)
        userinfo_form = self.userinfo_form(instance=request.user.userinfo)
        pmethod_form = self.pmethod_form(instance=request.user.userinfo.payment_method)

        return render(request, self.template_name, {
            'user_form': user_form,
            'userinfo_form': userinfo_form,
            'pmethod_form': pmethod_form,
        })

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST, instance=request.user)
        userinfo_form = self.userinfo_form(request.POST, instance=request.user.userinfo)
        pmethod_form = self.pmethod_form(request.POST, instance=request.user.userinfo.payment_method)
        if user_form.is_valid() and userinfo_form.is_valid() and pmethod_form.is_valid():
            user_form.save()
            userinfo_form.save()
            pmethod_form.save()
            messages.success(request, _('Your account was successfully updated!'))
            return redirect('user')
        else:
            messages.error(request, _('Please correct the error below.'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'userinfo_form': userinfo_form,
            'pmethod_form': pmethod_form
        })


# User Registration View
class RegisterView(View):
    register_form = RegisterForm
    template_name = 'register.html'

    decorators = [transaction.atomic]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        register_form = self.register_form()

        return render(request, self.template_name, {'register_form': register_form})

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        register_form = self.register_form(self.request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            # add userinfo data
            user.userinfo.user_type = register_form.cleaned_data.get('user_type')
            user.save()
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, {'register_form': register_form})


# User Add Credit Card View
class AddCreditCardView(View):
    pmethod_form = PaymentMethodForm
    creditcard_formset = CreditCardFormSet
    template_name = 'creditcard_form.html'

    decorators = [transaction.atomic, login_required]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(instance=request.user.userinfo.payment_method)
        creditcard_formset = self.creditcard_formset(instance=request.user.userinfo.payment_method)

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "creditcard_formset": creditcard_formset,
        })

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(request.POST, instance=request.user.userinfo.payment_method)
        creditcard_formset = self.creditcard_formset(request.POST, instance=request.user.userinfo.payment_method)

        if creditcard_formset.is_valid() and pmethod_form.is_valid():
            pmethod_form.save()
            creditcard_formset.save()
            return redirect('user')

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "creditcard_formset": creditcard_formset,
        })


# User Add Bank Account View
class AddBankAccountView(View):
    pmethod_form = PaymentMethodForm
    bankaccount_formset = BankAccountFormSet
    template_name = 'bankaccount_form.html'

    decorators = [transaction.atomic, login_required]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(instance=request.user.userinfo.payment_method)
        bankaccount_formset = self.bankaccount_formset(instance=request.user.userinfo.payment_method)

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "bankaccount_formset": bankaccount_formset,
        })

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(request.POST, instance=request.user.userinfo.payment_method)
        bankaccount_formset = self.bankaccount_formset(request.POST, instance=request.user.userinfo.payment_method)

        if bankaccount_formset.is_valid() and pmethod_form.is_valid():
            pmethod_form.save()
            bankaccount_formset.save()
            return redirect('user')

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "bankaccount_formset": bankaccount_formset,
        })


# Produce Item View
class ProduceItemListView(ListView):
    model = ProduceItem
    template_name = 'produce_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# Detail view for produce item
class ProduceItemDetailView(DetailView):
    model = ProduceItem
    template_name = 'produce_item.html'

    def get_context_data(self, **kwargs):
        context = super(ProduceItemDetailView, self).get_context_data(**kwargs)
        context['form'] = AddProduceItemToCart()
        return context


# POST/Form view for produce item adding to cart
class ProduceItemFormView(SingleObjectMixin, FormView):
    form_class = AddProduceItemToCart
    model = ProduceItem
    template_name = 'produce_item.html'

    def post(self, request, *args, **kwargs):
        addCart_form = self.form_class(self.request.POST)
        if addCart_form.is_valid():
            # retrieve quantity
            quantity = addCart_form.cleaned_data.get('quantity')

            # retrieve currently viewed produce item
            self.object = self.get_object()

            # update or create cart item
            obj, created = CartItem.objects.update_or_create(
                # filter with these unique values
                cart__exact=request.user.cart, produce_item__exact=self.object,
                # fields to update and their values
                defaults={
                    'produce_item': self.object,
                    'cart': request.user.cart,
                    'quantity': quantity,
                    'unit_cost': self.object.price,
                    'subtotal': self.object.price * quantity,   # compute subtotal
                }
            )

            UpdateCartDetails(request.user.cart)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('produce-list')
        #return reverse_lazy('produce-item', kwargs={'pk': self.object.pk})


# combine form view with detail view (https://docs.djangoproject.com/en/2.0/topics/class-based-views/mixins/)
class ProduceItemView(View):
    template_name = 'produce_item.html'

    def get(self, request, *args, **kwargs):
        view = ProduceItemDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProduceItemFormView.as_view()
        return view(request, *args, **kwargs)


# Cart View
class CartView(View):
    #model = Cart
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        UpdateCartDetails(request.user.cart)
        view = CartListView.as_view()
        return view(request, *args, **kwargs)

'''
    def post(self, request, *args, **kwargs):
        view = DeleteCartItemView.as_view()
        return view(request, *args, **kwargs)
'''


class CartListView(ListView):
    model = Cart
    template_name = 'cart.html'


# Delete Item from cart view (via URL)
class DeleteCartItemView(DeleteView):
    model = CartItem
    template_name = 'cart.html'
    success_url = reverse_lazy('cart')
