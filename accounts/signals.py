# accounts/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def load_department_levels(sender, user, request, **kwargs):
    qs = user.department_memberships.select_related("department").all()
    request.session["department_levels"] = {
        mem.department.id: mem.level for mem in qs
    }

@receiver(user_logged_out)
def clear_department_levels(sender, request, **kwargs):
    request.session.pop("department_levels", None)
