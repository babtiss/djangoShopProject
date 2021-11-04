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

    # @action(methods=['put'], detail=False, url_path='current_cart/add_to_cart/(?P<product_id>\d+)')
    # def product_add_to_cart(self, *args, **kwargs):
    #     cart = self._get_cart(self.request.user)
    #     product = get_object_or_404(Product, id=kwargs['product_id'])
    #     cart_product, created = self._get_or_create_cart_product(self.request.user.customer, cart, product)
    #     if created:
    #         cart.products.add(cart_product)
    #         cart.save()
    #         return Response({"detail": "Товар добавлен в корзину", "added": True})
    #     return Response({'detail': "Товар уже в корзине", "added": False}, status=status.HTTP_400_BAD_REQUEST)
    #
    # @action(methods=["patch"], detail=False,
    #         url_path='current_cart/change_qty/(?P<qty>\d+)/(?P<cart_product_id>\d+)')
    # def product_change_qty(self, *args, **kwargs):
    #     cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
    #     cart_product.qty = int(kwargs['qty'])
    #     cart_product.save()
    #     cart_product.cart.save()
    #     return Response(status=status.HTTP_200_OK)
    #
    # @action(methods=["put"], detail=False, url_path='current_cart/remove_from_cart/(?P<cproduct_id>\d+)')
    # def product_remove_from_cart(self, *args, **kwargs):
    #     cart = self._get_cart(self.request.user)
    #     cproduct = get_object_or_404(CartProduct, id=kwargs['cproduct_id'])
    #     cart.products.remove(cproduct)
    #     cproduct.delete()
    #     cart.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
