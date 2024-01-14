from django.contrib import admin
from .models import Aircraft, AircraftModel, Seat


# Register your models here.
class AircraftAdmin(admin.ModelAdmin):
    model = Aircraft
    list_display = ('name', 'model', 'total_seats', 'window_seats', 'extra_legroom_seats', 'aisle_seats')
    list_filter = ('total_seats', )


class AircraftModelAdmin(admin.ModelAdmin):
    model = AircraftModel
    list_display = ('name', 'manufacturer', 'manufacturer_year')
    list_filter = ('manufacturer', 'manufacturer_year')


class SeatModelAdmin(admin.ModelAdmin):
    model = Seat
    list_display = ('name',)


admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(AircraftModel, AircraftModelAdmin)
admin.site.register(Seat, SeatModelAdmin)
