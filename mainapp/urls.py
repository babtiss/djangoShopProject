from django.contrib.auth.views import LogoutView
from django.urls import path

from mainapp.views import *

urlpatterns = [
    path('', BaseView.as_view(), name='mainapp_home'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='products_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty-in-cart/<str:slug>/', ChangeQtyView.as_view(),
         name='change_qty_in_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile')
]