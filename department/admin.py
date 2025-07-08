#department/admin.py
from django.contrib import admin
from .models import (
    DepartmentCategory, DepartmentType, DepartmentRegion,
    UserProfile, OnDutyChangeLog, Department,
    DepartmentMembership, ApprovalLimit
)

admin.site.register(DepartmentCategory)
admin.site.register(DepartmentType)
admin.site.register(DepartmentRegion)
admin.site.register(UserProfile)
admin.site.register(OnDutyChangeLog)
admin.site.register(Department)
admin.site.register(DepartmentMembership)
admin.site.register(ApprovalLimit)
