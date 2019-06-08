from django.forms import ModelForm


def dynamic_form_generator(admin_class, form_add=False):
    """ create dynamic model form """
    class Meta:
        model = admin_class.model
        fields = '__all__'
        if not form_add:
            exclude = admin_class.readonly_fields

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control', "id": 'id-%s' % field_name})
        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm', (ModelForm, ), {'Meta': Meta, '__new__': __new__})
    return dynamic_form

