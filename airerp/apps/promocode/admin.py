from django.contrib import admin
from .models import PromoCode


# Register your models here.
class PromoCodeAdmin(admin.ModelAdmin):
    model = PromoCode


admin.site.register(PromoCode, PromoCodeAdmin)
