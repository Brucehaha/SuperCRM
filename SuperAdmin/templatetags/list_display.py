import datetime

from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def table_list(obj, admin_class):
    '''
    get the fk relate model and filter the related data set
    :param obj:
    :param admin_class:
    :return:
    '''
    _html = ''
    cell = ''
    app_name = admin_class.model._meta.app_label
    model_name = admin_class.model._meta.model_name

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
            elif col == 'image_tag':
                cell = getattr(obj, col)()

            else:
                cell = getattr(obj, col)

                choice = obj._meta.get_field(col).choices
                if any(choice):
                    cell = getattr(obj, "get_%s_display" % col)()

            if admin_class.list_display.index(col) == 0:

                 _html += "<td><a href='/superadmin/%s/%s/%s/edit'>%s</a></td>" % (app_name, model_name, obj.id, cell)
            else:
                _html += "<td class='align-middle'>%s</td>" % cell
    else:
        _html = "<td><a href='/superadmin/%s/%s/%s/edit'>%s</a></td>" % (app_name, model_name, obj.id, obj)

    return mark_safe(_html)


@register.simple_tag
def list_display(col, admin_class=None):
    res = col
    if '__' in col:
        res = col.split('__')[1]
    elif col == "image_tag":
        res =admin_class.model.image_tag.short_description
    elif "_" in res:
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
    elif column_obj.get_internal_type() == "ForeignKey":
        new_opts = column_obj.related_model.objects.values_list('id', 'name')
        options.extend(list(new_opts))
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


@register.simple_tag
def sort_by_column(column, curr_column, count0):
    if column in curr_column:
        # need to get the order(acs dcs)
        last_sorted_index = curr_column[column]
        if last_sorted_index.startswith('-'):
            curr_sorted_index = last_sorted_index.strip('-')

        else:
            curr_sorted_index = '-%s' % last_sorted_index
        return curr_sorted_index
    else:
        return count0


@register.simple_tag
def render_filter_icon(column, curr_column):
    """render filter icon """
    if column in curr_column:  # column been sorted,
        last_sort_index = curr_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'down'
        else:
            arrow_direction = 'up'
        ele = '''<i class ="fas fa-sort-%s"> </i"></span>''' % arrow_direction
        return mark_safe(ele)
    return ''


@register.simple_tag
def render_filtered_args(admin_class, render_html=True):
    """ concat link """
    if admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += '&%s=%s' %(k, v)
        if render_html:
            return mark_safe(ele)
    else:
        return ''


@register.simple_tag
def render_form_field(f):
    """ return field type"""
    return type(f.field.widget).__name__


@register.simple_tag
def get_m2m_avalaible_data(field_name, form_obj,  admin_class):
    """
    find all the m2m available values of that field
    :param field: form field object
    :param form_obj: django modelform instance
    :param admin_class: admin_class with model object
    :return: value list the related m2m value not selected
    """
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    try:
        selected_data = set(getattr(form_obj.instance, field_name).all())
    except TypeError:
        selected_data = set()

    return obj_list - selected_data


@register.simple_tag
def get_selected_m2m_data(field_name, form_obj):
    """
    find all the m2m available values of that field
    :param field: form field object
    :param form_obj: django modelform instance
    :param admin_class: admin_class with model object
    :return: value list the related m2m value selected
    """
    try:
        selected_data = set(getattr(form_obj.instance, field_name).all())
    except TypeError:
        selected_data = set()
    return selected_data


@register.simple_tag
def get_readonly_value(form, field_name):
    """
    :param form: form from edit view
    :param field_name: field name in readonly_field
    :return: instance field value
    """
    v = getattr(form.instance, field_name)
    # field_type = form.instance._meta.get_field(field_name).get_internal_type()
    return v


@register.simple_tag
def render_image(form_obj, field_name):
    url = None
    try:
        v = getattr(form_obj.instance, field_name)
        print(v.url)
        print(type(v))
        url = v.url
    except KeyError as e:
        print(e)
    except ValueError as e:
        print(e)
    else:
        print('Could not find image due to unknown reason')
    finally:
        return url

@register.simple_tag
def get_selected_m2m_image(form_obj, field_name):
    images = []
    related_model = None
    response = False
    if hasattr(form_obj, 'instance'):
        field_obj = form_obj.instance._meta.get_field(field_name)
        field_type = field_obj.get_internal_type()
        if field_type == "ManyToManyField":
            queryset = getattr(form_obj.instance, field_name).all()
            response = True
            related_model = field_obj.related_model()
            for field in related_model._meta.get_fields():
                if field.get_internal_type() == 'FileField':
                    for i in queryset:
                        image_field = getattr(i, field_name)
                        images.append((i.id, image_field.url))

    return (response, images, related_model._meta.model_name, related_model._meta.app_label)


