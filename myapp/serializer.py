from .models import Product, Supplier
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pid', 'pname', 'category', 'mfd', 'price', 'supplier')

