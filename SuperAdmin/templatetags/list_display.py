from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def table_list(col, obj):
    cell = None
    # get the fk relate model and filter the related data set

    if "__" in col:
        colNameList = []
        list_obj = None
        col_list = col.split('__')
        # field name of model with foreignkey pointed to ojb model class
        colName = col_list[1]
        # table name with foreignkey point to obj model class
        modelName = col_list[0]
        # model instance id
        obj_id = obj.id
        # filer condition to get he instance set by id
        condition = {'%s_id' % obj._meta.model_name: obj_id}
        # get the tables which have foreign key point to obj model class
        for m in obj._meta._relation_tree:
            if m.model._meta.model_name == modelName:
                list_obj = m.model.objects.filter(**condition)
                break

        if list_obj is not None:
            for x in list_obj:
                choice = x._meta.get_field(colName).choices
                if any(choice):
                    colNameList.append(getattr(x, "get_%s_display" % colName)())
                    continue
                colNameList.append(getattr(x, colName))
        if any(colNameList):
            cell = "/".join([str(x) for x in colNameList])

    else:
        cell = getattr(obj, col)
        choice = obj._meta.get_field(col).choices
        if any(choice):
            cell = getattr(obj, "get_%s_display" % col)()

    return mark_safe("<td>%s</td>" % cell)


@register.simple_tag
def list_display(data):
    res = data
    if '__' in data:
        res = data.split('__')[1]
    if "_" in res:
        res = res.replace('_', ' ')
    return res


@register.simple_tag
def formlize(f, kls):
    field = getattr(kls.model, f, False)
    _html = ''
    if not field:
        return None
    choices = kls.model._meta.get_field(f).choices
    print(choices)
    if any(choices):
        _html = "<select name=%s>" % f
        for c in choices:
            print(c)
            _html += "<option value=%s>%s</option>" % (c[0], c[1])
        _html += "</select>"
    return mark_safe(_html)
