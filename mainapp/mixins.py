from django.views.generic import View

from mainapp.models import *


class NavbarMixin(View):

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
        self.categories = Category.objects.all()
        self.cart = cart
        self.customer = customer
        return super().dispatch(request, *args, **kwargs)