# department/models.py
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size(value):
    limit = 100 * 1024 * 1024  # 100 MB
    if value.size > limit:
        raise ValidationError('File too large. Size must be ≤ 100 MB.')


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    is_on_duty = models.BooleanField(default=False)
    job_title = models.CharField(
        max_length=100,
        default="Not Defined Yet",
        blank=True,
        help_text="User’s job title (e.g. Sales Manager)."
    )

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        title = self.job_title or "Not Defined Yet"
        return f"{name} ({title})"


class DepartmentType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DepartmentSubtype(models.Model):
    """
    A subtype belonging to exactly one DepartmentType.
    """
    type = models.ForeignKey(
        DepartmentType,
        on_delete=models.CASCADE,
        related_name="subtypes"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("type", "name")
        ordering = ["type__name", "name"]
        verbose_name = "Department Subtype"

    def __str__(self):
        return f"{self.type.name} → {self.name}"


class DepartmentRegion(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class OnDutyChangeLog(models.Model):
    who_changed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="duty_changes_made"
    )
    target_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="duty_change_logs"
    )
    old_value = models.BooleanField()
    new_value = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.who_changed.get_full_name() or self.who_changed.username
        whom = self.target_profile.user.get_full_name() or self.target_profile.user.username
        status = "ON" if self.new_value else "OFF"
        return f"{who} set {whom} {status}-duty at {self.timestamp:%Y-%m-%d %H:%M}"


class Department(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.PROTECT,
        help_text="Leave blank for a top-level department"
    )
    dept_type = models.ForeignKey(
        DepartmentType,
        on_delete=models.PROTECT,
        related_name="departments"
    )
    subtype = models.ForeignKey(
        DepartmentSubtype,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="departments",
        help_text="Optional subtype (must belong to selected Type)"
    )
    region = models.ForeignKey(DepartmentRegion, on_delete=models.PROTECT)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="DepartmentMembership",
        related_name="departments"
    )

    class Meta:
        unique_together = ('parent', 'name')

    def clean(self):
        # 1) Enforce subtype → type consistency
        if self.subtype and self.subtype.type_id != self.dept_type_id:
            raise ValidationError({
                "subtype": "Subtype must belong to the selected Department Type."
            })
        # 2) Enforce max nesting of 3
        depth = 1
        p = self.parent
        while p:
            depth += 1
            if depth > 3:
                raise ValidationError("Departments may only be nested up to 3 levels.")
            p = p.parent

    def __str__(self):
        prefix = "— " * (self.get_level() - 1)
        return f"{prefix}{self.name}"

    def get_level(self):
        lvl = 1
        p = self.parent
        while p:
            lvl += 1
            p = p.parent
        return lvl


class DepartmentMembership(models.Model):
    L1 = 1
    L2 = 2
    L3 = 3
    LEVEL_CHOICES = [
        (L1, "L1 (Top)"),
        (L2, "L2 (Mid)"),
        (L3, "L3 (Base)"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="department_memberships"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department_memberships"
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        default=L3,
        help_text="1=Top, 2=Mid, 3=Base"
    )

    class Meta:
        unique_together = ("user", "department")
        ordering = ["department__name", "level"]

    def __str__(self):
        return f"{self.user.username} in {self.department.name} at L{self.level}"


class ApprovalLimit(models.Model):
    LEVEL_CHOICES = [(3, "L3 (Rep)"), (2, "L2 (Manager)"), (1, "L1 (Director)")]
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="approval_limits",
        help_text="Department this limit applies to"
    )
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES)
    max_amount = models.PositiveIntegerField(help_text="Max quote total auto-approved")

    class Meta:
        unique_together = [('department', 'level')]
        ordering = ['department__name', '-level']
        verbose_name = 'Approval Limit'
        verbose_name_plural = 'Approval Limits'

    def __str__(self):
        return f"{self.department.name} – L{self.level} up to ₹{self.max_amount}"
