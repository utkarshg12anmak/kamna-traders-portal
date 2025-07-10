#catalog/admin.py
from django.contrib import admin
from .models import Category, UnitOfMeasure, TaxRate, Brand, Item, ItemImage, UPC


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    readonly_fields = ('image_tag',)
    fields = ('image', 'alt_text')

    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return ''
    image_tag.short_description = 'Preview'


class UPCInline(admin.TabularInline):
    model = UPC
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'name', 'type', 'l1_category', 'l2_category', 'status', 'gst_rate', 'brand'
    )
    list_filter = ('type', 'status', 'l1_category', 'l2_category', 'gst_rate', 'brand')
    search_fields = ('sku', 'name', 'hsn_code')
    readonly_fields = ('sku', 'created_at', 'updated_at')
    autocomplete_fields = (
        'l1_category', 'l2_category', 'uom', 'gst_rate', 'brand',
        'weight_uom', 'dimension_uom'
    )
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'type', 'status')
        }),
        ('Categories & Codes', {
            'fields': ('l1_category', 'l2_category', 'hsn_code')
        }),
        ('UoM & Tax', {
            'fields': ('uom', 'gst_rate')
        }),
        ('Brand & Pricing', {
            'fields': ('brand',)
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'weight_uom', 'length', 'width', 'height', 'dimension_uom')
        }),
        ('Audit', {
            'fields': ('sku', 'created_at', 'updated_at', 'created_by', 'updated_by')
        }),
    )
    inlines = [ItemImageInline, UPCInline]

    def save_model(self, request, obj, form, change):
        # Set created_by / updated_by
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
