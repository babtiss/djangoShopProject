from django.views.generic import ListView

from .models import Category, Product


class CategoryListView(ListView):
    paginate_by = 2
    model = Category


class ProductListView(ListView):
    paginate_by = 2
    model = Product
