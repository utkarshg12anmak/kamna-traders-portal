from django import template

register = template.Library()

@register.filter
def dict_get(obj, key):
    """
    Given either a dict or a model instance, return obj[key] or getattr(obj, key).
    """
    try:
        # try dict-style lookup
        return obj.get(key, '')
    except Exception:
        # fallback to attribute lookup
        return getattr(obj, key, '')
