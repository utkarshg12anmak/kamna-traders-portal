#kamna_traders/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import RedirectView
from accounts.views import dashboard

def home(request):
    return HttpResponse("Kamna Traders Portal is up and running!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('', include('accounts.urls')),
    
]
