from repository import models
from SuperAdmin.sites import site


class TicketAdmin(object):
    lsit_display = ['name']


site.register(models.Ticket, TicketAdmin)
