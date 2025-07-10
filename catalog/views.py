# catalog/views.py

from django.views.generic import TemplateView
from web_pages.models import PageItem

class CatalogHomeView(TemplateView):
    template_name = 'Catalog/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 1) Grab your top-level “Catalog” PageItem
        catalog = PageItem.objects.get(
            name__iexact='Catalog',
            parent__isnull=True
        )

        # 2) Into context, push that as current_item
        ctx['current_item'] = catalog

        # 3) And its children as nav_items (ordered however you like)
        ctx['nav_items'] = catalog.children.all().order_by('order', 'name')

        return ctx
