from django.contrib import admin
from .models import Flight, FlightService


# Register your models here.
class FlightServiceAdminInline(admin.StackedInline):
    model = FlightService
    extra = 0


class FlightServiceAdmin(admin.ModelAdmin):
    model = FlightService
    list_display = ('flight', 'service', 'price')
    list_filter = ('flight', 'service')


class FlightAdmin(admin.ModelAdmin):
    model = Flight
    inlines = (FlightServiceAdminInline,)
    list_display = ('code', 'seat_class', 'departure_from', 'arrival_to', 'departure_time', 'arrival_time', 'aircraft', 'status')
    list_filter = ('code', 'departure_from', 'arrival_to', 'aircraft', 'status')


admin.site.register(FlightService, FlightServiceAdmin)
admin.site.register(Flight, FlightAdmin)
