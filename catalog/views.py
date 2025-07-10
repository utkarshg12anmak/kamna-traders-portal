# catalog/views.py
from django.views.generic import TemplateView
from web_pages.models import PageItem

class CatalogHomeView(TemplateView):
    template_name = 'Catalog/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # look up your top-level “Catalog” page
        catalog = PageItem.objects.get(
            name__iexact='Catalog',
            parent__isnull=True
        )

        # push it & its children into the template
        ctx['current_item'] = catalog
        ctx['nav_items']    = catalog.children.all().order_by('order', 'name')

        return ctx
