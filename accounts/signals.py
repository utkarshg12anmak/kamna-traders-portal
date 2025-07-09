# accounts/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from web_pages.models import PageItem  # import the PageItem model

@receiver(user_logged_in)
def load_department_levels(sender, user, request, **kwargs):
    qs = user.department_memberships.select_related("department").all()
    request.session["department_levels"] = {
        mem.department.id: mem.level for mem in qs
    }

@receiver(user_logged_out)
def clear_department_levels(sender, request, **kwargs):
    request.session.pop("department_levels", None)


@receiver(user_logged_in)
def load_user_mappings(sender, user, request, **kwargs):
    """
    On login, store:
      - department_levels: { department_id: level, ... }
      - page_items:      [ list of allowed PageItem IDs ]
    """
    # 1) Build department → level
    memberships = user.department_memberships.select_related("department").all()
    dept_levels = {m.department.id: m.level for m in memberships}
    request.session["department_levels"] = dept_levels

    # 2) Find all subtypes via those departments
    #    first grab each department’s assigned subtype (if any)
    subtype_ids = [
        m.department.subtype_id
        for m in memberships
        if m.department.subtype_id is not None
    ]

    # 3) Query PageItems linked to those subtypes
    page_item_ids = list(
        PageItem.objects
            .filter(subtypes__in=subtype_ids)
            .distinct()
            .values_list("id", flat=True)
    )
    request.session["page_items"] = page_item_ids

    

@receiver(user_logged_out)
def clear_user_mappings(sender, request, **kwargs):
    for key in ("department_levels", "page_items"):
        request.session.pop(key, None)
