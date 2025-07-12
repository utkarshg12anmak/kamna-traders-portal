#catalog/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
import random, string

from django.db import models
from django.conf import settings

class TimeStampedUserModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name="%(class)ss_created",
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name="%(class)ss_updated",
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True

def item_image_upload_to(instance, filename):
    """
    Build S3 upload path based on environment (separate dev/prod folders) and item SKU.
    """
    env = getattr(settings, 'ENVIRONMENT', 'dev')  # e.g. 'dev' or 'prod'
    base_folder = 'dev' if env == 'dev' else 'prod'
    return f"{base_folder}/items/{instance.item.sku}/{filename}"

from .models import TimeStampedUserModel

class Category(TimeStampedUserModel):
    """
    Single model for L1/L2 categories (self-referential). Only two levels used in UI.
    """
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='children'
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['parent__id', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UnitOfMeasure(TimeStampedUserModel):
    """
    Units for measuring items, weight, dimensions, etc.
    """
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = 'Unit of Measure'
        verbose_name_plural = 'Units of Measure'

    def __str__(self):
        return self.abbreviation or self.name


class TaxRate(TimeStampedUserModel):
    """
    GST/Tax rates for items.
    """
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage rate, e.g. 18.00 for 18%")

    class Meta:
        verbose_name = 'Tax Rate'
        verbose_name_plural = 'Tax Rates'

    def __str__(self):
        return f"{self.name} ({self.rate}%)"


class Brand(TimeStampedUserModel):
    """
    Manufacturer or brand of an item.
    """
    name = models.CharField(max_length=255, unique=True)    

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Core product/item model with auto-generated SKU, audit, status etc.
    """
    TYPE_GOODS = 'goods'
    TYPE_SERVICE = 'service'
    TYPE_CHOICES = [
        (TYPE_GOODS, 'Goods'),
        (TYPE_SERVICE, 'Service'),
    ]

    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    sku = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        help_text="10-char alphanumeric code derived from name+categories"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    l1_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='l1_items',
        limit_choices_to={'parent__isnull': True},
        help_text="Top-level category"
    )
    l2_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='l2_items',
        limit_choices_to={'parent__isnull': False},
        help_text="Second-level category"
    )
    hsn_code = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    # New fields
    uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name='items',
        help_text="Unit of measure for stock/quantity"
    )
    gst_rate = models.ForeignKey(
        TaxRate,
        on_delete=models.PROTECT,
        related_name='items',
        help_text="GST/Tax rate applied to this item"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='items',
        blank=True, null=True,
        help_text="Item's brand or manufacturer"
    )

    # Physical attributes
    weight = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True,
        help_text="Weight of item in its unit"
    )
    weight_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name='weight_items',
        blank=True, null=True,
        help_text="Unit of measure for weight"
    )
    length = models.DecimalField(
        max_digits=10, decimal_places=0,
        blank=True, null=True
    )
    width = models.DecimalField(
        max_digits=10, decimal_places=0,
        blank=True, null=True
    )
    height = models.DecimalField(
        max_digits=10, decimal_places=0,
        blank=True, null=True
    )
    dimension_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name='dimension_items',
        blank=True, null=True,
        help_text="Unit of measure for dimensions"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='items_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='items_updated'
    )

    class Meta:
        ordering = ['sku']

    def save(self, *args, **kwargs):
        # only generate the SKU when the row is first inserted
        if self._state.adding:  
            self.sku = self._generate_sku()
        super().save(*args, **kwargs)

    def _generate_sku(self):
        # Derive a reproducible, 10-char alphanumeric from name + categories
        seed_str = f"{self.name}:{self.l1_category.name}:{self.l2_category.name}"
        rnd = random.Random(seed_str)
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(rnd.choices(alphabet, k=10))

    def __str__(self):
        return f"{self.sku} – {self.name}"  


class ItemImage(models.Model):
    """
    Images for Items, stored on S3 under separate env folders.
    """
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=item_image_upload_to)
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.item.sku}"  


class UPC(models.Model):
    """
    UPC codes mapping one-to-many: each UPC belongs to exactly one Item, but an Item can have many UPCs.
    """
    item = models.ForeignKey(Item, related_name='upcs', on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.code
