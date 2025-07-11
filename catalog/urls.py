# catalog/urls.py

from django.urls import path, include
from . import views
from django.views.generic import RedirectView
from .views import CatalogHomeView
from .views import BrandListView
from .views import UOMListView
from .views import ItemListView


app_name = 'catalog'

urlpatterns = [
    # Redirect “/catalog/” → “/catalog/home/”
    path(
        '',
        RedirectView.as_view(pattern_name='catalog-home', permanent=False),
        name='catalog-index'
    ),

    # Your actual home page
    path('home/', CatalogHomeView.as_view(), name='catalog-home'),
    path('items/', ItemListView.as_view(), name='catalog-items'),
    path('brands/', BrandListView.as_view(), name='catalog-brands'),
    path('bom/', ItemListView.as_view(), name='catalog-bom'),     
    path('uom/', UOMListView.as_view(), name='catalog-uom'),         

]

