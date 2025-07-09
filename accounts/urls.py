#accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'  # our new template
    ), name='login'),
]

