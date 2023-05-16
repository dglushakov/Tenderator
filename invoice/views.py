import io

from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .models import Device, Category, Manufacturer
import os
import pandas
from io import StringIO

from django.conf import settings as django_settings
from django.http import HttpResponse
from .resources import DeviceResource


# Create your views here.
class DetailView(generic.DetailView):
    model = Device
    template_name = 'invoice/device_details.html'


def index(request):
    devices = Device.objects.all().order_by('device_category', 'device_manufacturer')

    devices_ordered = {}

    for device in devices:
        if device.device_category not in devices_ordered.keys():
            devices_ordered[device.device_category] = {}
        if device.device_manufacturer not in devices_ordered[device.device_category].keys():
            devices_ordered[device.device_category][device.device_manufacturer] = []

        devices_ordered[device.device_category][device.device_manufacturer].append(device)

    print(devices_ordered)
    context = {
        'devices': devices,
        'devices_ordered': devices_ordered,

    }

    return render(request, 'invoice/device_list.html', context)


def save_invoice_to_csv(request, categories_and_manufacturers=''):
    print('start')
    print(categories_and_manufacturers)
    print(django_settings.STATIC_ROOT)
    import csv

    # with open('invoice.csv', 'w', newline='', encoding='utf-8') as csvfile:
    try:
        filepath = os.path.join(django_settings.STATIC_ROOT, 'invoice.csv')
        csvfile = open(filepath, 'w', newline='', encoding='utf-8')
    except FileNotFoundError:
        filepath = os.path.join('static', 'invoice.csv')
        csvfile = open(filepath, 'w', newline='', encoding='utf-8')

    with csvfile as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')

        for elem in categories_and_manufacturers.split(";"):
            category = elem[:elem.find(":")].strip()
            manufacturer = elem[elem.find(":") + 1:].strip()
            writer.writerow([category])
            writer.writerow([manufacturer])
            print(elem, " --", category, '+', manufacturer, sep='')

            devices = Device.objects \
                .filter(device_category__category_name=category, device_manufacturer__manufacturer_name=manufacturer) \
                .order_by('device_category', 'device_manufacturer')

            for device in devices:
                writer.writerow([device.device_name, device.device_description, "some other data"])

    return FileResponse(open(filepath, 'rb'))
    # return redirect('invoice:index')


def save_invoice_as_xls(request, categories_and_manufacturers=''):
    columns_list = ['id', 'device_name', 'device_description', 'device_manufacturer', 'device_category']
    results_date_frame = pandas.DataFrame([], columns=columns_list)

    for elem in categories_and_manufacturers.split(";"):
        category = elem[:elem.find(":")].strip()
        manufacturer = elem[elem.find(":") + 1:].strip()
        devices = Device.objects \
            .filter(device_category__category_name=category, device_manufacturer__manufacturer_name=manufacturer) \
            .order_by('device_category', 'device_manufacturer')

        for device in devices:
            attributes_dict = {}
            for column_name in columns_list:
                attributes_dict[column_name] = getattr(device, column_name)

            results_date_frame = pandas.concat([results_date_frame, pandas.DataFrame(attributes_dict, index=[0])],
                                               ignore_index=True)

    with io.BytesIO() as b:
        with pandas.ExcelWriter(b) as writer:
            results_date_frame.to_excel(writer, index=False)

        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = 'attachment; filename=invoice.xlsx'
        return res
