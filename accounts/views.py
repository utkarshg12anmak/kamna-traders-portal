#accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    # You can pass in dynamic data here later (e.g. user role)
    options = [
        #{ 'label': 'Warehouses',    'url': 'warehouses:index'    },
        # 'label': 'Sales',         'url': 'sales:index'         },
        #{ 'label': 'Manufacturing', 'url': 'manufacturing:index' },
        # add more as you build out apps…
    ]
    return render(request, 'dashboard.html', { 'options': options })
