from django.contrib import admin
from .models import Latest

class LatestAdmin(admin.ModelAdmin):
    list_display = ('plate', 'fps', 'status')

admin.site.register(Latest, LatestAdmin)
