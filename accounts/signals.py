# accounts/signals.py
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

@receiver(user_logged_out)
def clear_user_session(sender, request, **kwargs):
    for key in ("username","first_name","last_name","job_title"):
        request.session.pop(key, None)
