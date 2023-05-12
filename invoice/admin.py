from django.contrib import admin

# Register your models here.
from .models import Device, Manufacturer, Category

# for import and export
from import_export.admin import ImportExportActionModelAdmin

from .resources import DeviceResource


class DeviceAdmin(ImportExportActionModelAdmin):
    resource_class = DeviceResource
    list_filter = ['device_manufacturer', 'device_category']
    list_display = ('device_name', 'device_category', 'device_manufacturer')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category)
