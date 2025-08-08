from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Brand, UOM, TaxRate

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
