from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def table_list(col, obj):
    cell = getattr(obj, col)
    return mark_safe("<td>%s</td>" % cell)

