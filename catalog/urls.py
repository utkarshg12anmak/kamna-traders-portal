# catalog/urls.py

from django.urls import path
from django.views.generic import RedirectView
from .views import CatalogHomeView
from .views import CatalogItemView
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, UnitOfMeasureViewSet, TaxRateViewSet, BrandViewSet, ItemViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('uoms', UnitOfMeasureViewSet)
router.register('taxrates', TaxRateViewSet)
router.register('brands', BrandViewSet)
router.register('items', ItemViewSet)

urlpatterns = [
    # Redirect “/catalog/” → “/catalog/home/”
    path(
        '',
        RedirectView.as_view(pattern_name='catalog-home', permanent=False),
        name='catalog-index'
    ),

    # Your actual home page
    path('home/', CatalogHomeView.as_view(), name='catalog-home'),
    path('items/', CatalogItemView.as_view(), name='catalog-items'),
    path('bom/', CatalogHomeView.as_view(), name='catalog-bom'),

]
