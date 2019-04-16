import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def table_list(obj, admin_class):
    # get the fk relate model and filter the related data set
    _html = ''
    cell = ''
    if admin_class.list_display:
        for col in admin_class.list_display:
            if "__" in col:
                colNameList = []
                list_obj = None
                #  model name and field name of model with foreignkey pointed to ojb model class
                model_name, col_name = col.split('__')
                # model instance id
                obj_id = obj.id
                # filer condition to get he instance set by id
                condition = {'%s_id' % obj._meta.model_name: obj_id}

                # get the tables which have foreign key point to obj model class
                for m in obj._meta._relation_tree:
                    if m.model._meta.model_name == model_name:
                        list_obj = m.model.objects.filter(**condition)
                        break

                if list_obj is not None:
                    for x in list_obj:
                        choice = x._meta.get_field(col_name).choices
                        if any(choice):
                            colNameList.append(getattr(x, "get_%s_display" % col_name)())
                            continue
                        colNameList.append(getattr(x, col_name))
                if any(colNameList):
                    cell = "/".join([str(x) for x in colNameList])

            else:
                cell = getattr(obj, col)
                choice = obj._meta.get_field(col).choices
                if any(choice):
                    cell = getattr(obj, "get_%s_display" % col)()
            _html += "<td>%s</td>" % cell
    else:
        _html = "<td>%s</td>" % obj

    return mark_safe(_html)


@register.simple_tag
def list_display(data):
    res = data
    if '__' in data:
        res = data.split('__')[1]
    if "_" in res:
        res = res.replace('_', ' ')
    return res


@register.simple_tag
def list_filter(f, kls):
    column_obj = kls.model._meta.get_field(f)
    _html = "<select name=%s>" % f
    options = [('', "All")]
    filter_value = kls.filter_conditions.get(f)
    is_time = False
    choices = column_obj.choices
    if any(choices):
        options.extend(choices)

    elif column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
        _html = "<select name='%s__gte'>" % f
        filter_value = kls.filter_conditions.get('%s__gte' % f)
        is_time = True
        time_obj = datetime.datetime.now()
        options.extend(
            [
                (time_obj, 'Today'),
                (time_obj - datetime.timedelta(7), '7 days'),
                (time_obj - datetime.timedelta(30), '1 month'),
                (time_obj - datetime.timedelta(90), '3 months'),
                (time_obj - datetime.timedelta(180), '6 months'),
                (time_obj - datetime.timedelta(180), 'YearToDay'),
            ]
        )
    else:
        return ''

    for o in options:
        time_to_str = str(o[0])
        if is_time:
            time_to_str = '' if not o[0] else '%s-%s-%s'%(o[0].year, o[0].month, o[0].day)
        selected = '' if time_to_str != filter_value else 'selected'

        _html += "<option %s value='%s'>%s</option>" %(selected, time_to_str, o[1])
    _html += "</select>"

    return mark_safe(_html)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()