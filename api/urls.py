from django.urls import path
from rest_framework.routers import SimpleRouter
from .main.views import *


urlpatterns = [
    path('product/', ProductList.as_view()),
    path('category/', CategoryList.as_view()),

]

