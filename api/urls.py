from django.urls import path
from rest_framework.routers import SimpleRouter

from .cart.views import CartViewSet
from .main.views import *

main_router = SimpleRouter()
urlpatterns = [
    path('product/', ProductList.as_view()),
    path('category/', CategoryList.as_view()),

]
main_router.register('cart', CartViewSet, basename='cart')
urlpatterns += main_router.urls
