from django.db import models


def calc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Sum('qty'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    if cart_data['qty__sum']:
        cart.number_of_products = cart_data['qty__sum']
    else:
        cart.number_of_products = 0
    cart.save()
