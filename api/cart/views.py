from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from mainapp.models import Cart, Customer, Product, CartProduct
from .serializers import CartSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    @staticmethod
    def _get_cart(user):
        cart = None
        if user.is_authenticated:
            customer = Customer.objects.filter(user=user).first()
            if not customer:
                customer = Customer.objects.create(user=user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer, final_price=0, number_of_products=0)
        return cart

    @staticmethod
    def _get_or_create_cart_product(customer, cart, product):

        cart_product, created = CartProduct.objects.get_or_create(
            user=customer,
            product=product,
            cart=cart
        )
        return cart_product, created

    @action(methods=["get"], detail=False)
    def current_cart(self, *args, **kwargs):
        cart = self._get_cart(self.request.user)
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data)

