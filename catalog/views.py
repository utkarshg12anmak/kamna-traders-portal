# catalog/views.py
from django.views.generic import TemplateView
from web_pages.models import PageItem
from rest_framework import viewsets, permissions
from .models import Category, UnitOfMeasure, TaxRate, Brand, Item, ItemImage, UPC
from .serializers import (
    CategorySerializer, UnitOfMeasureSerializer, TaxRateSerializer, 
    BrandSerializer, ItemSerializer, ItemImageSerializer, UPCSerializer
)
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
    
class CatalogItemView(TemplateView):
    template_name = 'Catalog/items.html'

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
    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

# repeat for UnitOfMeasure, TaxRate, Brand

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().select_related(
        'l1_category','l2_category','uom','gst_rate','brand'
    ).prefetch_related('images','upcs')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

