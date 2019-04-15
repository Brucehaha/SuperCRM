from . import models
from SuperAdmin.sites import site


class TestAdmin(object):
    list_display = ('name', 'timestamp')

site.register(models.test, TestAdmin)
