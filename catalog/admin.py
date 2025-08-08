from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Brand

@admin.register(Brand)
class BrandAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'website', 'created_at', 'updated_at', 'version')
    search_fields = ('name', 'website', 'contact')
    list_filter = ('created_at', 'updated_at')

    # Do not allow manual edits to audit fields
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'updated_by', 'version', 'deleted_at'
    )

    def save_model(self, request, obj, form, change):
        # Ensure audit fields are system-driven
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user if request.user.is_authenticated else None
        if not obj.updated_by:
            obj.updated_by = request.user if request.user.is_authenticated else None
        super().save_model(request, obj, form, change)
