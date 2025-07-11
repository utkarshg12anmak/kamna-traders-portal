# Generated by Django 5.2.4 on 2025-07-09 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("department", "0002_alter_departmentmembership_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="department",
            name="category",
        ),
        migrations.AlterField(
            model_name="approvallimit",
            name="level",
            field=models.PositiveIntegerField(
                choices=[(3, "L3 (Rep)"), (2, "L2 (Manager)"), (1, "L1 (Director)")]
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="dept_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="departments",
                to="department.departmenttype",
            ),
        ),
        migrations.CreateModel(
            name="DepartmentSubtype",
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
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subtypes",
                        to="department.departmenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Department Subtype",
                "ordering": ["type__name", "name"],
                "unique_together": {("type", "name")},
            },
        ),
        migrations.AddField(
            model_name="department",
            name="subtype",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional subtype (must belong to selected Type)",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="departments",
                to="department.departmentsubtype",
            ),
        ),
        migrations.DeleteModel(
            name="DepartmentCategory",
        ),
    ]
