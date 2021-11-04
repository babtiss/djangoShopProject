from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.contrib import messages

from mainapp.forms import OrderForm, LoginForm, RegistrationForm
from mainapp.mixins import *
from mainapp.utils import calc_cart


class BaseView(CustomerAndCartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        data = {
            'categories': categories,
            'cart': self.cart,
        }

        return render(request, 'mainapp/layout.html', data)


class ProductDetailView(CustomerAndCartMixin, DetailView):
    slug_url_kwarg = 'slug'
    model = Product
    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['categories'] = self.categories
        product_slug = self.kwargs['slug']
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.filter(cart=self.cart, product=product).first()
        context['product_in_cart'] = True if cart_product else False
        return context


class CategoryDetailView(CustomerAndCartMixin, DetailView):
    slug_url_kwarg = 'slug'
    template_name = 'mainapp/category_detail.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=Category.objects.get(slug=self.kwargs['slug']))
        context['cart'] = self.cart
        context['categories'] = self.categories
        return context


class CartView(CustomerAndCartMixin, View):

    def get(self, request, *args, **kwargs):
        data = {
            'customer': self.customer,
            'cart': self.cart,
            'categories': self.categories,
        }
        return render(request, 'mainapp/cart.html', data)


class AddToCartView(CartProductMixin, View):

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if self.created:
            self.cart.products.add(self.cart_product)
            calc_cart(self.cart)

        return HttpResponseRedirect(reverse('products_detail', args=(slug,)))


class DeleteFromCartView(CartProductMixin, View):

    def get(self, request, *args, **kwargs):
        self.cart.products.remove(self.cart_product)
        self.cart_product.delete()
        calc_cart(self.cart)
        if '/cart/' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect('/cart/')
        else:
            return HttpResponseRedirect(reverse('products_detail', args=(self.slug,)))


class ChangeQtyView(CartProductMixin, View):

    def post(self, request, *args, **kwargs):
        qty = request.POST.get('qty')
        self.cart_product.qty = int(qty)
        self.cart_product.save()
        calc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CheckoutView(CustomerAndCartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        form = OrderForm(request.POST or None)
        data = {
            'customer': customer,
            'cart': self.cart,
            'form': form,
        }
        return render(request, 'mainapp/checkout.html', data)


class MakeOrderView(CustomerAndCartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        form = OrderForm(request.POST)
        if form.is_valid():
            self.cart.in_order = True
            self.cart.save()
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.address = form.cleaned_data['address']
            new_order.phone = form.cleaned_data['phone']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.comment = form.cleaned_data['comment']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.cart = self.cart
            new_order.save()

            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CustomerAndCartMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        data = {
            'customer': self.customer,
            'cart': self.cart,
            'categories': self.categories,
            'form': form,
        }
        return render(request, 'mainapp/login.html', data)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        data = {
            'customer': self.customer,
            'cart': self.cart,
            'categories': self.categories,
            'form': form,
        }
        return render(request, 'mainapp/login.html', data)


class RegistrationView(CustomerAndCartMixin, View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        data = {
            'customer': self.customer,
            'cart': self.cart,
            'categories': self.categories,
            'form': form,
        }
        return render(request, 'mainapp/registration.html', data)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        data = {
            'customer': self.customer,
            'cart': self.cart,
            'categories': self.categories,
            'form': form,
        }
        return render(request, 'mainapp/registration.html', data)


class ProfileView(CustomerAndCartMixin, View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(customer=self.customer).order_by('-created_date')
        data = {
            'orders': (enumerate(orders, 1)),
            'cart': self.cart,
            'categories': self.categories,
            'customer': self.customer,
        }
        return render(request, 'mainapp/profile.html', data)
