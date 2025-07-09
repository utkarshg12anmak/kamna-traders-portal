#web_pages/views.py
from django.shortcuts import render, get_object_or_404
from .models import PageItem

def dashboard(request):
    # 1) All level-1 items:
    items = PageItem.objects.filter(parent__isnull=True).order_by("name")
    # 2) Allowed IDs from session (might be missing or empty)
    allowed = set(request.session.get("page_items", []))
    return render(request, "dashboard.html", {
        "dashboard_items": items,
        "allowed_page_ids": allowed,
    })

def page_item(request, slug):
    # Find the item by slugified name
    # You could store slug in the model if you prefer—this is a quick hack.
    all_items = PageItem.objects.all()
    item = next(
        (pi for pi in all_items if pi.name.lower().replace(" ", "-") == slug),
        None
    )
    if not item:
        raise Http404
    # You could load children or related data here
    return render(request, "page_item.html", {"item": item})
