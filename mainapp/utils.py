from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models

MAX_IMAGE_SIZE = 2
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600


def validate_image(obj):
    filesize = obj.file.size
    if filesize > MAX_IMAGE_SIZE * 1024 * 1024:
        raise ValidationError(f"Max file size is {MAX_IMAGE_SIZE} MB")


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
