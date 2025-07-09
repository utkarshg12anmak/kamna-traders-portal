# kamna_traders/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    # (optional) explicitly point at your login URL
    login_url = "login"
    # (optional) the name of the “next” param
    redirect_field_name = "next"

    # … any other methods/context you already have …
