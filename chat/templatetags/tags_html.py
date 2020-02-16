from django import template
from django.contrib.auth import get_user_model
register = template.Library()


@register.filter
def addclass(field, css):
    field.field.widget.attrs['class'] = field.field.widget.attrs.get('class', '') + ' ' + css
    return field


@register.filter
def placeholder(field, value):
    field.field.widget.attrs['placeholder'] = value
    return field

@register.filter
def user_display_name(user):
    """Returns user's full name or his username if the full name is not available."""
    if isinstance(user, get_user_model()):
        return user.get_full_name() or user.username
    return 'Anonymous'