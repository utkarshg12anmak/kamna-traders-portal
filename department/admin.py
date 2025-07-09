# department/admin.py

from django.contrib import admin
from .models import (
    DepartmentType,
    DepartmentSubtype,
    DepartmentRegion,
    UserProfile,
    OnDutyChangeLog,
    Department,
    DepartmentMembership,
    ApprovalLimit,
)

# register the simple models
admin.site.register(DepartmentType)
admin.site.register(DepartmentSubtype)
admin.site.register(DepartmentRegion)
admin.site.register(UserProfile)
admin.site.register(OnDutyChangeLog)
admin.site.register(ApprovalLimit)

# inline for Dept ↔ Membership
class DepartmentMembershipInline(admin.TabularInline):
    model = DepartmentMembership
    extra = 1
    fields = ("user", "level")
    autocomplete_fields = ("user",)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ("name", "dept_type", "subtype", "region")
    list_filter   = ("dept_type", "subtype", "region")
    search_fields = ("name",)
    inlines       = [DepartmentMembershipInline]
    fieldsets     = [
        (None, {"fields": ["name", "parent"]}),
        ("Classification", {"fields": ["dept_type", "subtype", "region"]}),
    ]

@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display        = ("user", "department", "level")
    list_filter         = ("department", "level")
    search_fields       = ("user__username", "department__name")
    autocomplete_fields = ("user", "department")
