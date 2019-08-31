from django.contrib import admin
from .models import Vehicle, System, Log

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate', 'v_type', 'owner', 'color', 'guard')

class LogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'reason', 'datetime_in', 'datetime_out', 'guard', 'status')

admin.site.register(Vehicle, VehicleAdmin)
# admin.site.register(System)
admin.site.register(Log, LogAdmin)
