#kamna_traders/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import RedirectView
from accounts.views import dashboard
from django.conf import settings
from django.contrib.auth.views import LogoutView
from web_pages import views as wp_views

def home(request):
    return HttpResponse("Kamna Traders Portal is up and running!")

urlpatterns = [
    path('admin/', admin.site.urls), 
    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),
    path('', include('accounts.urls')),

    # Dashboard home
    path("", wp_views.dashboard, name="dashboard"),

    # Page‐item pages (e.g. /catalog/, /sales/, etc.)
    path("<slug:slug>/", wp_views.page_item, name="page-item"),
    path('catalog/', include('catalog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

