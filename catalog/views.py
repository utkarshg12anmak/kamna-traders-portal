# catalog/views.py
from django.views.generic import TemplateView
from web_pages.models import PageItem
from rest_framework import viewsets, permissions
from .models import Category, UnitOfMeasure, TaxRate, Brand, Item, ItemImage, UPC
from django.views.generic import ListView
from django.template.loader import render_to_string   # ← add this
from .forms import BrandForm
from django.urls import reverse
from .models import Brand
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
    
class ItemListView(ListView):
    model = Item
    template_name = "catalog/items.html"
    context_object_name = "object_list"

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        ctx['brand_create_url'] = reverse('catalog:brand-bulk-create')
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


from rest_framework import viewsets, permissions
from .models import Category, UnitOfMeasure, TaxRate, Brand, Item
from .serializers import (
    CategorySerializer, UnitOfMeasureSerializer, TaxRateSerializer,
    BrandSerializer, ItemSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaxRateViewSet(viewsets.ModelViewSet):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer
    permission_classes = [permissions.IsAuthenticated]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().select_related(
        'l1_category','l2_category','uom','gst_rate','brand'
    ).prefetch_related('images','upcs')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .models import Brand

@require_POST
def bulk_create_brands(request):
    # Grab all inputs named "brand_name" (we’ll name them that in the form)
    names = request.POST.getlist('brand_name')
    # Strip/ignore blanks
    names = [n.strip() for n in names if n.strip()]
    # Bulk create those brands
    Brand.objects.bulk_create([Brand(name=n) for n in names])
    # Redirect back to your items page
    return redirect('catalog:item-list')  # adjust to your actual URL name
