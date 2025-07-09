# webpages/models.py

from django.db import models

class PageItem(models.Model):
    """
    A node in a simple hierarchy.  Optional icon_name references a static file.
    """
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        null=True, blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        help_text="Leave blank for top-level pages"
    )
    icon_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Static filename (e.g. 'warehouse.png') under your static folder"
    )

    class Meta:
        verbose_name = "Web Page Item"
        verbose_name_plural = "Web Page Items"
        ordering = ("parent__id", "name")

    def __str__(self):
        return self.name

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
