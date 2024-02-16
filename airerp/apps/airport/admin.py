from django.contrib import admin
from .models import City, Airport


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('name', 'country')
    list_filter = ('country', )


class AirportAdmin(admin.ModelAdmin):
    model = Airport
    list_display = ('code', 'name', 'latitude', 'longitude', 'city')
    list_filter = ('city__country', )


admin.site.register(City, CityAdmin)
admin.site.register(Airport, AirportAdmin)
