# catalog/urls.py

# catalog/urls.py
from django.urls import path
from django.views.generic import RedirectView
from .views import CatalogHomeView

urlpatterns = [
    # Redirect “/catalog/” → “/catalog/home/”
    path(
        '',
        RedirectView.as_view(pattern_name='catalog-home', permanent=False),
        name='catalog-index'
    ),

    # Your actual home page
    path('home/', CatalogHomeView.as_view(), name='catalog-home'),
]
