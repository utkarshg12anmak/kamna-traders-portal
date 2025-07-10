# web_pages/admin.py

from django.contrib import admin
from .models import PageItem

@admin.register(PageItem)
class PageItemAdmin(admin.ModelAdmin):
    list_display  = ("name", "parent", "order", "icon_name")
    list_filter  = ("parent",)
    search_fields = ("name", "icon_name")
    list_editable = ("order",)

    def path(self, obj):
        # Collect all ancestor names, then self
        names = []
        node = obj
        while node:
            names.insert(0, node.name)
            node = node.parent
        return " → ".join(names)
    path.short_description = "Hierarchy"
