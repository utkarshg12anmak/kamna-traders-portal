# webpages/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import PageItem

@admin.register(PageItem)
class PageItemAdmin(admin.ModelAdmin):
    list_display = ("indented_name", "icon_name")
    list_filter  = ("parent",)
    search_fields = ("name", "icon_name")
    ordering     = ("parent__id", "name")

    def indented_name(self, obj):
        return format_html(
            "{}{}",
            "&nbsp;&nbsp;&nbsp;" * obj.get_level(),
            obj.name
        )
    indented_name.short_description = "Name"
