# catalog/urls.py

from django.urls import path, include
from . import views
from django.views.generic import RedirectView
from .views import CatalogHomeView
from .views import CatalogItemView
from .views import ItemListView
from rest_framework.routers import DefaultRouter
from .views import TaxRateViewSet
from .views import manage_uoms
from .views import BrandListView


app_name = 'catalog'


router = DefaultRouter()
router.register(r"taxrates", TaxRateViewSet)


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
    path('brands/', BrandListView.as_view(), name='catalog-brands'),
    path('bom/', CatalogHomeView.as_view(), name='catalog-bom'),     
    path("api/", include(router.urls)),
    path('manage-uoms/', manage_uoms, name='manage_uoms'),

]

