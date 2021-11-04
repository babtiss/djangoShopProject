from django.views.generic import View

from mainapp.models import *


class CustomerAndCartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        cart = None
        customer = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer, final_price=0, number_of_products=0)
        self.cart = cart
        self.customer = customer
        self.categories = Category.objects.all()
        return super().dispatch(request, *args, **kwargs)


class CartProductMixin(View):
    def dispatch(self, request, *args, **kwargs):
        cart = None
        customer = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer, final_price=0, number_of_products=0)
        self.cart = cart
        self.slug = kwargs.get('slug')
        product = Product.objects.get(slug=self.slug)
        self.cart_product, self.created = CartProduct.objects.get_or_create(
            owner=self.cart.owner,
            cart=self.cart,
            product=product
        )
        self.customer = customer
        self.categories = Category.objects.all()
        return super().dispatch(request, *args, **kwargs)
