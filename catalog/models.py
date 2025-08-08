import uuid
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from .utils import get_current_user
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from .managers import NotDeletedManager
import string, secrets

class AuditModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   related_name='%(class)s_created', on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   related_name='%(class)s_updated', on_delete=models.SET_NULL)
    deleted_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        is_create = self._state.adding or not self.pk
        if is_create:
            if not self.created_by and getattr(user, 'is_authenticated', False):
                self.created_by = user
            # ensure initial version
            self.version = self.version or 1
        else:
            self.version = (self.version or 0) + 1
        # Always set updated_by to the current user if authenticated
        if getattr(user, 'is_authenticated', False):
            self.updated_by = user
        super().save(*args, **kwargs)

class Brand(AuditModel):
    name = models.CharField(max_length=120, unique=True)
    logo_url = models.URLField(blank=True)
    website = models.URLField(blank=True)
    contact = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# ─── UOM and TaxRate ───────────────────────────────────────────────────────────
class UOM(AuditModel):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100)
    decimals = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code}"

class TaxRate(AuditModel):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.rate}%)"

# ─── Category (max depth 2) ───────────────────────────────────────────────────
class Category(AuditModel):
    name = models.CharField(max_length=120)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='children'
    )
    # New active flag
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['parent', 'name'], name='uq_category_parent_name')
        ]

    @property
    def level(self) -> int:
        # Level-1 = Root (no parent); Level-2 = has parent
        return 1 if self.parent is None else 2

    def clean(self):
        super().clean()
        # Enforce max depth of Level-2
        if self.parent and self.parent.parent is not None:
            raise ValidationError({'parent': 'Only two levels allowed (Root -> Child). This parent already has a parent.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Attach default managers that hide soft-deleted rows
Brand.add_to_class('objects', NotDeletedManager())
Category.add_to_class('objects', NotDeletedManager())
UOM.add_to_class('objects', NotDeletedManager())
TaxRate.add_to_class('objects', NotDeletedManager())

class ItemStatus(models.TextChoices):
    DRAFT = 'Draft', 'Draft'
    ACTIVE = 'Active', 'Active'
    ARCHIVED = 'Archived', 'Archived'

ALPHABET = string.ascii_uppercase + string.digits

def generate_sku() -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(10))

class Item(AuditModel):
    sku = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=8, choices=ItemStatus.choices, default=ItemStatus.DRAFT)

    category = models.ForeignKey('catalog.Category', on_delete=models.PROTECT, related_name='items')
    brand = models.ForeignKey('catalog.Brand', on_delete=models.PROTECT, related_name='items')
    uom = models.ForeignKey('catalog.UOM', on_delete=models.PROTECT)
    tax_rate = models.ForeignKey('catalog.TaxRate', on_delete=models.PROTECT)

    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    image_url = models.URLField(blank=True)

    for_sale = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)
    is_manufactured = models.BooleanField(default=False)

    history = HistoricalRecords(inherit=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['status']),
            models.Index(fields=['brand']),
            models.Index(fields=['category'])
        ]
        ordering = ['name']

    def clean(self):
        super().clean()
        if self.category:
            # Must be a Level-2 category (must have a parent)
            if getattr(self.category, 'parent', None) is None:
                raise ValidationError({'category': 'Items must be assigned to a Level-2 category (select a child category).'})
            # Max depth guard (<=2)
            if getattr(self.category.parent, 'parent', None) is not None:
                raise ValidationError({'category': 'Only categories up to Level-2 are allowed.'})

    def save(self, *args, **kwargs):
        creating = self._state.adding
        if creating and not self.sku:
            # collision-safe generation (retry up to 5x)
            for _ in range(5):
                candidate = generate_sku()
                if not Item.objects.filter(sku=candidate).exists():
                    self.sku = candidate
                    break
        # Validate business rules after ensuring SKU present
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sku} — {self.name}"

# Attach Item default manager
Item.add_to_class('objects', NotDeletedManager())
