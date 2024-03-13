# Сериализаторы нужны для преобразования одного вида данных в другие виды
from rest_framework import serializers
from .models import Product, Order, Supplier, Pos_supply, Supply


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'pk',
            'customer_surname',
            'customer_name',
            'customer_patronymic',
            'delivery_address',
            'delivery_type',
            'creation_date',
            'finish_date',
            'product',
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'name',
            'description',
            'price',
            'creation_date',
            'image',
            'isActive',
            'category',
            'tag',
            'parameter',
        ]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'representor_surname',
            'representor_name',
            'representor_patronymic',
            'representor_phone_number'
        ]

class ProductSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'price'
        ]

class Pos_supplySerializer(serializers.ModelSerializer):
    product = ProductSupplySerializer(read_only=True)
    class Meta:
        model = Pos_supply
        fields = [
            'product',
            'quantity'
        ]


class SupplySerializer(serializers.ModelSerializer):
    pos_supply_set = Pos_supplySerializer(read_only=True, many=True)
    supplier = serializers.HyperlinkedRelatedField(read_only=True, view_name='supplier-detail')

    class Meta:
        model = Supply
        fields = [
            'pk',
            'date',
            'supplier',
            'pos_supply_set'
        ]