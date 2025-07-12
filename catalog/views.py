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
    paginate_by = 10

    form_class   = BrandForm
    success_url  = reverse_lazy('catalog:catalog-brands')

    def get_queryset(self):
        qs = super().get_queryset()
        # pull all brand‐IDs from ?brands=…&brands=…
        brand_ids = self.request.GET.getlist("brands")
        if brand_ids:
            qs = qs.filter(id__in=brand_ids)
        return qs  

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["all_brands"] = Brand.objects.order_by("name")

        # your existing “add” form
        if 'form' not in ctx:
            ctx['form'] = self.get_form()

        # per‐row edit forms
        ctx['brand_forms'] = {
            brand.id: BrandForm(instance=brand)
            for brand in ctx['brands']
        }

        catalog = PageItem.objects.get(name__iexact="Catalog", parent__isnull=True)
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.order_by("order", "name")
        return ctx        


    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        brand_id = data.get('id')  # we’ll include <input name="id">
        instance = Brand.objects.filter(pk=brand_id).first() if brand_id else None
        form = BrandForm(data, instance=instance)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            brand = form.save(user=request.user)
            if is_ajax:
                # return the updated brand data
                return JsonResponse({
                    'success': True,
                    'brand': {
                        'id':   brand.id,
                        'name': brand.name,
                        'created_at': brand.created_at.strftime('%Y-%m-%d %H:%M'),
                        'created_by': brand.created_by.get_full_name(),
                        'updated_at': brand.updated_at.strftime('%Y-%m-%d %H:%M'),
                        'updated_by': brand.updated_by.get_full_name(),
                    }
                })
            return super().form_valid(form)

        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import UnitOfMeasure
from .forms import UnitOfMeasureForm
from web_pages.models import PageItem

class UnitOfMeasureListView(LoginRequiredMixin, FormMixin, ListView):
    """
    Shows the list of UOMs and handles create‐and‐edit POSTs via the same URL,
    setting created_by/updated_by on each save.
    """
    model               = UnitOfMeasure
    template_name       = "catalog/uom.html"
    context_object_name = "uoms"
    paginate_by         = 10

    form_class  = UnitOfMeasureForm
    success_url = reverse_lazy('catalog:catalog-uom')
    
    def get_queryset(self):
        qs = super().get_queryset()
        # pull all brand‐IDs from ?brands=…&brands=…
        uom_ids = self.request.GET.getlist("uoms")
        if uom_ids:
            qs = qs.filter(id__in=uom_ids)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # “New UoM” form
        if 'form' not in ctx:
            ctx['form'] = self.get_form()
        # per‐row “Edit UoM” forms
        ctx['uom_forms'] = {
            uom.id: UnitOfMeasureForm(instance=uom)
            for uom in ctx['uoms']
        }

        ctx["all_uoms"] = UnitOfMeasure.objects.order_by("name")

        # sidebar/nav
        catalog = PageItem.objects.get(name__iexact="Catalog", parent__isnull=True)
        ctx['current_item'] = catalog
        ctx['nav_items']    = catalog.children.order_by('order','name')
        return ctx

    def post(self, request, *args, **kwargs):
        """
        If `id` is in POST we edit that UoM, otherwise create new.
        Ajax => JSON; regular => redirect.
        """
        data      = request.POST.copy()
        uom_id    = data.get('id')
        instance  = UnitOfMeasure.objects.filter(pk=uom_id).first() if uom_id else None
        form      = UnitOfMeasureForm(data, instance=instance)
        is_ajax   = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            # commit=False so we can set audit fields
            uom = form.save(commit=False)
            if not uom.pk:               # brand-new record
                uom.created_by = request.user
            uom.updated_by = request.user
            uom.save()

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'uom': {
                        'id':   uom.id,
                        'name': uom.name,
                        'abbr': uom.abbreviation,
                    }
                })
            return super().form_valid(form)

        # form invalid
        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)



# catalog/views.py
from django.urls        import reverse_lazy
from django.views.generic      import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http        import JsonResponse

from web_pages.models   import PageItem
from .models            import TaxRate
from .forms             import TaxRateForm


class TaxRateListView(LoginRequiredMixin, FormMixin, ListView):
    model               = TaxRate
    template_name       = "catalog/taxrates.html"
    context_object_name = "taxrates"
    paginate_by         = 10

    form_class  = TaxRateForm
    success_url = reverse_lazy('catalog:catalog-tax-rates')

    def get_queryset(self):
        qs = super().get_queryset()
        # optional multi-filter on ?rates=1&rates=2…
        rate_ids = self.request.GET.getlist("rates")
        if rate_ids:
            qs = qs.filter(id__in=rate_ids)
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # all for the multi‐select filter
        ctx["all_rates"] = TaxRate.objects.order_by("name")

        # brand‐style “add” form
        if 'form' not in ctx:
            ctx['form'] = self.get_form()

        # per‐row edit forms
        ctx['rate_forms'] = {
            tr.id: TaxRateForm(instance=tr)
            for tr in ctx['taxrates']
        }

        # sidebar/nav (unchanged)
        catalog = PageItem.objects.get(
            name__iexact="Catalog",
            parent__isnull=True
        )
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.order_by("order", "name")
        return ctx

    def post(self, request, *args, **kwargs):
        data      = request.POST.copy()
        rate_id   = data.get('id')
        instance  = TaxRate.objects.filter(pk=rate_id).first() if rate_id else None

        form      = TaxRateForm(data, instance=instance)
        is_ajax   = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            tr = form.save(user=request.user)
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'taxrate': {
                        'id':   tr.id,
                        'name': tr.name,
                        'rate': str(tr.rate),
                    }
                })
            return super().form_valid(form)

        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)


from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from web_pages.models import PageItem
from .models import Category
from .forms  import CategoryForm

class CategoryListView(LoginRequiredMixin, FormMixin, ListView):
    model               = Category
    template_name       = "catalog/categories.html"
    context_object_name = "categories"
    paginate_by         = 10

    form_class  = CategoryForm    # should inherit AuditFormMixin
    success_url = reverse_lazy('catalog:manage_categories')

    def get_queryset(self):
        qs = super().get_queryset()
        # pull selected name‐IDs and parent‐IDs from ?names=…&names=… and ?parents=…&parents=…
        name_ids   = self.request.GET.getlist('names')
        parent_ids = self.request.GET.getlist('parents')

        if name_ids:
            qs = qs.filter(id__in=name_ids)

        if parent_ids:
            qs = qs.filter(parent__id__in=parent_ids)

        return qs.order_by('parent__id', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # All categories for the multi-select dropdown        
        ctx['all_categories'] = Category.objects.order_by('name')
        ctx['all_parents']    = Category.objects.filter(parent__isnull=True).order_by('name')
        # “New Category” form
        if 'form' not in ctx:
            ctx['form'] = self.get_form()

        # Per-row “Edit” forms
        ctx['category_forms'] = {
            cat.id: CategoryForm(instance=cat)
            for cat in ctx['categories']
        }

        # Sidebar/nav (unchanged)
        catalog = PageItem.objects.get(name__iexact="Catalog", parent__isnull=True)
        ctx["current_item"] = catalog
        ctx["nav_items"]    = catalog.children.order_by("order","name")
        return ctx

    def post(self, request, *args, **kwargs):
        data     = request.POST.copy()
        cat_id   = data.get('id')
        instance = Category.objects.filter(pk=cat_id).first() if cat_id else None

        form     = self.form_class(data, instance=instance)
        is_ajax  = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            category = form.save(user=request.user)
            if is_ajax:
                return JsonResponse({
                  'success': True,
                  'category': {
                    'id':     category.id,
                    'name':   category.name,
                    'parent': category.parent.id if category.parent else None,
                    'created_at': category.created_at.strftime('%Y-%m-%d %H:%M'),
                    'created_by': category.created_by.get_full_name(),
                    'updated_at': category.updated_at.strftime('%Y-%m-%d %H:%M'),
                    'updated_by': category.updated_by.get_full_name(),
                  }
                })
            return super().form_valid(form)

        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
