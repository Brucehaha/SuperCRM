

class BaseAdminSite(object):
    verbose_name = None


class InlineModelAdmin(BaseAdminSite):
    model = None


