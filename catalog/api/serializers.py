from rest_framework import serializers
from catalog.models import Item, Brand, Category, UOM, TaxRate

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = ('id','sku','created_at','updated_at','version')
        fields = ('id','sku','name','description','status','category','brand','uom','tax_rate','unit_price','image_url','for_sale','is_purchased','is_manufactured','created_at','updated_at','version')

    def validate(self, attrs):
        # Ensure related objects are active
        for field, Model in [('brand', Brand), ('category', Category), ('uom', UOM), ('tax_rate', TaxRate)]:
            obj = attrs.get(field) or getattr(self.instance, field, None)
            if obj and (getattr(obj, 'is_active', True) is False or obj.deleted_at is not None):
                raise serializers.ValidationError({field: 'Selected value is inactive.'})
        # Category must be Level-2 (has a parent)
        cat = attrs.get('category') or getattr(self.instance, 'category', None)
        if cat is not None and cat.parent is None:
            raise serializers.ValidationError({'category': 'Items must be assigned to a Level-2 category (child).'})
        return attrs
