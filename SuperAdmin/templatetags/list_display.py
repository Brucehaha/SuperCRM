from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def table_list(col, obj):
    col_name = col
    item = obj
    list_obj = ''
    # get the fk relate model and filter the related data set
    if "__" in col:
        col_list = col.split('__')
        col_name = col_list[1]
        id = obj.id
        condition = {'%s_id' % obj._meta.model_name: id}
        for m in obj._meta._relation_tree:
            if m.model._meta.model_name == col_list[0]:
                list_obj = m.model.objects.filter(condition)
                break
    choice = item._meta.get_field(col_name).choices
    cell = getattr(obj, col)
    if len(choice) != 0:
        cell = getattr(obj, "get_%s_display" % col)()
    return mark_safe("<td>%s</td>" % cell)

