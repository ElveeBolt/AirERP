from django.contrib import admin
from .models import Service, Baggage


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('name', )


class BaggageAdmin(admin.ModelAdmin):
    model = Baggage
    list_display = ('name', )


admin.site.register(Service, ServiceAdmin)
admin.site.register(Baggage, BaggageAdmin)

