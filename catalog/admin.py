from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Brand, UOM, TaxRate, Category, Item
from django import forms

# Reusable admin that makes audit fields read-only and system-driven
class AuditAdmin(SimpleHistoryAdmin):
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'updated_by', 'version', 'deleted_at'
    )

    def save_model(self, request, obj, form, change):
        # Set audit fields using the current user (no manual input)
        if obj._state.adding and not obj.created_by and request.user.is_authenticated:
            obj.created_by = request.user
        if request.user.is_authenticated:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Brand)
class BrandAdmin(AuditAdmin):
    list_display = ('name', 'website', 'is_active', 'created_at', 'updated_at', 'version')
    list_editable = ('is_active',)
    search_fields = ('name', 'website', 'contact')
    list_filter = ('is_active', 'created_at', 'updated_at')

@admin.register(UOM)
class UOMAdmin(AuditAdmin):
    list_display = ('code', 'name', 'decimals', 'is_active', 'created_at', 'updated_at', 'version')
    list_filter = ('is_active', 'decimals', 'created_at', 'updated_at')
    search_fields = ('code', 'name')

@admin.register(TaxRate)
class TaxRateAdmin(AuditAdmin):
    list_display = ('title', 'rate', 'is_active', 'created_at', 'updated_at', 'version')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description')

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','parent','is_active']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Parent can only be a Root category (no parent)
        self.fields['parent'].queryset = Category.objects.filter(parent__isnull=True, deleted_at__isnull=True)

@admin.register(Category)
class CategoryAdmin(AuditAdmin):
    form = CategoryAdminForm
    list_display = ('name','parent','is_active','created_at','updated_at','version')
    list_editable = ('is_active',)
    list_filter = ('parent', 'is_active', 'created_at','updated_at')
    search_fields = ('name',)

class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        # Hide audit columns from the form entirely
        exclude = ('created_by','updated_by','deleted_at','version','created_at','updated_at')
        widgets = {
            'sku': forms.TextInput(attrs={'readonly': 'readonly'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(is_active=True, deleted_at__isnull=True)
        # Only Level-2 categories (must have a parent)
        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False, is_active=True, deleted_at__isnull=True)
        self.fields['uom'].queryset = UOM.objects.filter(is_active=True, deleted_at__isnull=True)
        self.fields['tax_rate'].queryset = TaxRate.objects.filter(is_active=True, deleted_at__isnull=True)

@admin.register(Item)
class ItemAdmin(AuditAdmin):
    form = ItemAdminForm
    list_display = ('sku','name','brand','category','unit_price','status','updated_at')
    list_filter = ('status','brand','category')
    search_fields = ('sku','name')
    # Keep all audit fields read-only (from base) and also lock sku
    readonly_fields = AuditAdmin.readonly_fields + ('sku',)
