

class BaseAdminSite(object):
    verbose_name = []
    list_display =[]
    list_filter =[]
    readonly_fields = []
    filter_horizontal = []
    image_fields = []
    field_order = []
    form_type = None
    actions = {"delete_selected_objs": 'Delete Selected'}
    readonly_table = False

    def delete_selected_objs(self, request, queryset):
        print(self)
        print(request, queryset)



