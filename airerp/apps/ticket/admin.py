from django.contrib import admin
from .models import Ticket, TicketService


# Register your models here.
class TicketServiceAdminInline(admin.StackedInline):
    model = TicketService
    extra = 0


class TicketServiceAdmin(admin.ModelAdmin):
    model = TicketService
    list_display = ('ticket', 'service')
    list_filter = ('ticket', 'service')


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ('code', 'user', 'flight', 'date_booked')
    inlines = (TicketServiceAdminInline,)


admin.site.register(TicketService, TicketServiceAdmin)
admin.site.register(Ticket, TicketAdmin)
