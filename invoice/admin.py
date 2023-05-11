from django.contrib import admin

# Register your models here.
from .models import Device, Manufacturer, Category

# for import and export
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


# for import and export
class DeviceResource(resources.ModelResource):
    device_manufacturer = fields.Field(column_name='device_manufacturer', attribute='device_manufacturer',
                                       widget=ForeignKeyWidget(Manufacturer, 'manufacturer_name'))

    device_category = fields.Field(column_name='device_category', attribute='device_category',
                                       widget=ForeignKeyWidget(Category, 'category_name'))
    class Meta:
        model = Device


class DeviceAdmin(ImportExportActionModelAdmin):
    resource_class = DeviceResource
    list_filter = ['device_manufacturer', 'device_category']
    list_display = ('device_name', 'device_category', 'device_manufacturer')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category)
