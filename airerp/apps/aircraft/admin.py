from django.contrib import admin
from .models import Aircraft, AircraftModel, AircraftManufacturerModel


# Register your models here.
class AircraftManufacturerModelAdmin(admin.ModelAdmin):
    model = AircraftManufacturerModel
    list_display = ('title',)


class AircraftAdmin(admin.ModelAdmin):
    model = Aircraft
    list_display = ('name', 'model', 'total_seats', 'window_seats', 'extra_legroom_seats', 'aisle_seats')
    list_filter = ('total_seats',)


class AircraftModelAdmin(admin.ModelAdmin):
    model = AircraftModel
    list_display = ('name', 'manufacturer', 'manufacturer_year')
    list_filter = ('manufacturer', 'manufacturer_year')


admin.site.register(AircraftManufacturerModel, AircraftManufacturerModelAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(AircraftModel, AircraftModelAdmin)
