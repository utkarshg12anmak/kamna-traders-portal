# catalog/serializers.py
from rest_framework import serializers
from .models import Category, UnitOfMeasure, TaxRate, Brand, Item, ItemImage, UPC

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'slug']

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['id', 'name', 'abbreviation']

class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = ['id', 'name', 'rate']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'alt_text']

class UPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = UPC
        fields = ['id', 'code']

class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)
    upcs   = UPCSerializer(many=True,    read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'sku', 'name', 'description', 'type',
            'l1_category', 'l2_category', 'hsn_code', 'status',
            'uom', 'gst_rate', 'brand',
            'weight', 'weight_uom', 'length', 'width', 'height', 'dimension_uom',
            'created_at', 'updated_at', 'created_by', 'updated_by',
            'images', 'upcs'
        ]
        read_only_fields = ['sku', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def create(self, validated_data):
        user = self.context['request'].user
        item = Item.objects.create(created_by=user, updated_by=user, **validated_data)
        return item

    def update(self, instance, validated_data):
        instance.updated_by = self.context['request'].user
        return super().update(instance, validated_data)
