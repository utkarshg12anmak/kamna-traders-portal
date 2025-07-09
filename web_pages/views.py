#web_pages/views.py
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import PageItem

def dashboard(request):
    """
    Renders the initial dashboard with L1 tiles (parent=None).
    """
    items = PageItem.objects.filter(parent__isnull=True).order_by("name")
    allowed = set(request.session.get("page_items", []))
    return render(request, "dashboard.html", {
        "dashboard_items": items,
        "allowed_page_ids": allowed,
    })


def page_item(request, slug):
    """
    Renders base.html for a given top-level page (slug).
    """
    # Find the PageItem whose slugified name matches
    all_items = PageItem.objects.filter(parent__isnull=True)
    item = get_object_or_404(
        all_items,
        name__iexact=slug.replace("-", " "),
    )

    # Its direct children become the sidebar nav
    nav_items = item.children.all().order_by("name")

    return render(request, "base.html", {
        "current_item": item,
        "nav_items": nav_items,
    })