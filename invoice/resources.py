from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Device, Manufacturer, Category


class DeviceResource(resources.ModelResource):
    device_manufacturer = fields.Field(column_name='device_manufacturer', attribute='device_manufacturer',
                                       widget=ForeignKeyWidget(Manufacturer, 'manufacturer_name'))

    device_category = fields.Field(column_name='device_category', attribute='device_category',
                                   widget=ForeignKeyWidget(Category, 'category_name'))

    class Meta:
        model = Device
        import_id_fields = ('id', 'device_name')
