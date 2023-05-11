from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .models import Device, Category, Manufacturer


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
    import csv

    with open('invoice.csv', 'w', newline='', encoding='utf-8') as csvfile:
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

    return redirect('invoice:index')


