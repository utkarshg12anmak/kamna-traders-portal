#kamna_traders/urls.py

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Kamna Traders Portal is up and running!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # ← catch the root URL
]
