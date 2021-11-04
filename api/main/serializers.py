from rest_framework import serializers
from mainapp.models import Product, Category, CartProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class GetProductOfCategorySerializer(CategorySerializer):
    products = serializers.SerializerMethodField()

    @staticmethod
    def get_products(obj):
        return ProductSerializer(Product.objects.filter(category=obj), many=True).data


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = '__all__'
