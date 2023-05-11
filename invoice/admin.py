from django.contrib import admin

# Register your models here.
from .models import Device, Manufacturer, Category


class DeviceAdmin(admin.ModelAdmin):
    # fields = ['device_name']
    list_filter = ['device_manufacturer', 'device_category']
    list_display = ('device_name', 'device_category', 'device_manufacturer')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category)
