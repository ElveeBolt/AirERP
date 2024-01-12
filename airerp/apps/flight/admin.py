from django.contrib import admin
from .models import Flight, FlightService, FlightSeat


# Register your models here.
class FlightServiceAdminInline(admin.StackedInline):
    model = FlightService
    extra = 0


class FlightSeatAdminInline(admin.StackedInline):
    model = FlightSeat
    extra = 0


class FlightServiceAdmin(admin.ModelAdmin):
    model = FlightService
    list_display = ('flight', 'service', 'price')
    list_filter = ('flight', 'service')


class FlightSeatAdmin(admin.ModelAdmin):
    model = FlightSeat
    list_display = ('flight', 'seat', 'price')
    list_filter = ('seat', 'price')


class FlightAdmin(admin.ModelAdmin):
    model = Flight
    inlines = (FlightServiceAdminInline, FlightSeatAdminInline)
    list_display = ('code', 'departure_from', 'arrival_to', 'departure_time', 'arrival_time', 'aircraft')
    list_filter = ('code', 'departure_from', 'arrival_to', 'aircraft')


admin.site.register(FlightService, FlightServiceAdmin)
admin.site.register(FlightSeat, FlightSeatAdmin)
admin.site.register(Flight, FlightAdmin)
