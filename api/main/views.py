from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductSerializer, CategorySerializer
from mainapp.models import Category, Product
from ..pagination import Pagination


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = Pagination


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Pagination
