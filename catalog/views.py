# catalog/views.py

from django.shortcuts import redirect
from django.forms import modelformset_factory
from django.views.generic import ListView
from .models import Item, TaxRate

from django.views.generic import TemplateView
from web_pages.models import PageItem
from .models import UnitOfMeasure
from django.template.loader import render_to_string
from django.http import HttpResponse


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

    def get_taxrate_formset(self, data=None):
        TaxRateFormSet = modelformset_factory(
            TaxRate,
            fields=("name", "rate"),    # adjust field names
            extra=1,
            can_delete=True
        )
        return TaxRateFormSet(data or None, queryset=TaxRate.objects.all())

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

class CatalogItemView(TemplateView):
    template_name = "catalog/items.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # find your top‐level “Catalog” page
        catalog = PageItem.objects.get(
            name__iexact="Catalog",
            parent__isnull=True
        )

        # inject for your sidebar/nav
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.all().order_by("order", "name")

        # if you want an actual Item list, you'd instead use a ListView—
        # but for now this just renders the template
        return ctx
    
from rest_framework import viewsets, permissions
from .models import TaxRate
from .serializers import TaxRateSerializer

class TaxRateViewSet(viewsets.ModelViewSet):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#manage_uoms view
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UnitOfMeasureFormSet

def manage_uoms(request):
    """
    Renders and processes a popup formset for creating/editing/deleting UoMs.
    """
    qs = UnitOfMeasure.objects.all()
    formset = UnitOfMeasureFormSet(request.POST or None, queryset=qs)

    # Debug logging
    if request.method == 'POST':
        print("POST DATA:", dict(request.POST))
        print("FORMSET ERRORS:", formset.errors)
        print("NON_FORM ERRORS:", formset.non_form_errors())

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            if is_ajax:
                return JsonResponse({'status': 'ok'})
            else:
                return redirect('catalog:manage_uoms')
        # If invalid
        if is_ajax:
            html = render_to_string('catalog/uom_manage_popup.html', {'formset': formset}, request=request)
            return HttpResponse(html)

    # On GET
    if is_ajax:
        html = render_to_string('catalog/uom_manage_popup.html', {'formset': formset}, request=request)
        return HttpResponse(html)
    return render(request, 'catalog/uom_manage_popup.html', {'formset': formset})