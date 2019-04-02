

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}

    def register(self, model_class, admin_class=None):
        print(model_class, admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class

site = AdminSite()