# Generated by Django 5.2.4 on 2025-07-10 11:27

import catalog.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
            },
        ),
        migrations.CreateModel(
            name="TaxRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Percentage rate, e.g. 18.00 for 18%",
                        max_digits=5,
                    ),
                ),
            ],
            options={
                "verbose_name": "Tax Rate",
                "verbose_name_plural": "Tax Rates",
            },
        ),
        migrations.CreateModel(
            name="UnitOfMeasure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("abbreviation", models.CharField(max_length=10, unique=True)),
            ],
            options={
                "verbose_name": "Unit of Measure",
                "verbose_name_plural": "Units of Measure",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="catalog.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ["parent__id", "name"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sku",
                    models.CharField(
                        editable=False,
                        help_text="10-char alphanumeric code derived from name+categories",
                        max_length=10,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("goods", "Goods"), ("service", "Service")],
                        max_length=7,
                    ),
                ),
                ("hsn_code", models.CharField(blank=True, max_length=50)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                        ],
                        default="draft",
                        max_length=8,
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        help_text="Weight of item in its unit",
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "length",
                    models.DecimalField(
                        blank=True, decimal_places=3, max_digits=10, null=True
                    ),
                ),
                (
                    "width",
                    models.DecimalField(
                        blank=True, decimal_places=3, max_digits=10, null=True
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        blank=True, decimal_places=3, max_digits=10, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        help_text="Item's brand or manufacturer",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="items",
                        to="catalog.brand",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="items_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "l1_category",
                    models.ForeignKey(
                        help_text="Top-level category",
                        limit_choices_to={"parent__isnull": True},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="l1_items",
                        to="catalog.category",
                    ),
                ),
                (
                    "l2_category",
                    models.ForeignKey(
                        help_text="Second-level category",
                        limit_choices_to={"parent__isnull": False},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="l2_items",
                        to="catalog.category",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="items_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "gst_rate",
                    models.ForeignKey(
                        help_text="GST/Tax rate applied to this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="items",
                        to="catalog.taxrate",
                    ),
                ),
                (
                    "dimension_uom",
                    models.ForeignKey(
                        blank=True,
                        help_text="Unit of measure for dimensions",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dimension_items",
                        to="catalog.unitofmeasure",
                    ),
                ),
                (
                    "uom",
                    models.ForeignKey(
                        help_text="Unit of measure for stock/quantity",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="items",
                        to="catalog.unitofmeasure",
                    ),
                ),
                (
                    "weight_uom",
                    models.ForeignKey(
                        blank=True,
                        help_text="Unit of measure for weight",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="weight_items",
                        to="catalog.unitofmeasure",
                    ),
                ),
            ],
            options={
                "ordering": ["sku"],
            },
        ),
        migrations.CreateModel(
            name="ItemImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to=catalog.models.item_image_upload_to),
                ),
                ("alt_text", models.CharField(blank=True, max_length=255)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="catalog.item",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UPC",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="upcs",
                        to="catalog.item",
                    ),
                ),
            ],
        ),
    ]
