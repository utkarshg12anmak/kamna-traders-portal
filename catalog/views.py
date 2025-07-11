# catalog/views.py

from django.shortcuts import redirect
from django.forms import modelformset_factory
from django.views.generic import ListView
from .models import Item

from django.views.generic import TemplateView
from web_pages.models import PageItem
from .models import UnitOfMeasure

class CatalogHomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # look up your top-level “Catalog” page
        catalog = PageItem.objects.get(
            name__iexact="Catalog",
            parent__isnull=True
        )

        # push it & its children into the template
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.all().order_by("order", "name")
        return ctx
        
class ItemListView(ListView):
    model = Item
    template_name = "Catalog/items.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["taxrate_formset"] = self.get_taxrate_formset()
        return ctx

    def post(self, request, *args, **kwargs):
        formset = self.get_taxrate_formset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("catalog:catalog-items")
        # if invalid, re-render with errors
        return self.render_to_response(self.get_context_data(taxrate_formset=formset))

    
# Add Manage Brands 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import Brand
from .models import UnitOfMeasure
from .forms import BrandForm
from web_pages.models import PageItem

class BrandListView(LoginRequiredMixin, FormMixin, ListView):
    """
    Shows the list of brands and handles new-brand POSTs via the same URL.
    """
    model = Brand
    template_name = "catalog/brands.html"
    context_object_name = "brands"

    form_class   = BrandForm
    success_url  = reverse_lazy('catalog:catalog-brands')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Ensure the form is in context
        if 'form' not in ctx:
            ctx['form'] = self.get_form()

        # Sidebar/nav context (if you still need it)
        catalog = PageItem.objects.get(name__iexact="Catalog", parent__isnull=True)
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.all().order_by("order", "name")
        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            brand = form.save()
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'brand': {
                        'id': brand.id,
                        'name': brand.name,
                        'created_at': brand.created_at.strftime('%Y-%m-%d %H:%M')
                    }
                })
            return super().form_valid(form)

        # form invalid
        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    

class UOMListView(LoginRequiredMixin, FormMixin, ListView):
    """
    Shows the list of brands and handles new-brand POSTs via the same URL.
    """
    model = UnitOfMeasure
    template_name = "catalog/uom.html"
    context_object_name = "uom"

    form_class   = BrandForm
    success_url  = reverse_lazy('catalog:catalog-uom')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Ensure the form is in context
        if 'form' not in ctx:
            ctx['form'] = self.get_form()

        # Sidebar/nav context (if you still need it)
        catalog = PageItem.objects.get(name__iexact="Catalog", parent__isnull=True)
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.all().order_by("order", "name")
        return ctx
