from django import conf
import importlib


def superadmin_auto_discover():

    for app in conf.settings.INSTALLED_APPS:
        try:
            mod = importlib.import_module('.superadmin', package=app)
            print(mod)
        except ImportError:
            pass
