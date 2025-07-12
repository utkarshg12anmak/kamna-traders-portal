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

@register.filter
def render_cell(value):
    """
    If this is a User (has get_full_name), show full name (fallback to username).
    Otherwise return the value as-is.
    """
    if hasattr(value, 'get_full_name'):
        full = value.get_full_name()
        return full or str(value)
    return value

@register.filter
def get_attr(obj, attr_name):
    """
    Given an object and attribute name (string), return getattr(obj, attr_name).
    """
    return getattr(obj, attr_name, '')

@register.filter
def get_item(dict_, key):
    return dict_.get(key)
