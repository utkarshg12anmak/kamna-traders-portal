# catalog/views.py

from django.shortcuts import render
from django.views.generic import TemplateView

class CatalogHomeView(TemplateView):
    template_name = 'Catalog/home.html'



# Create your views here.
