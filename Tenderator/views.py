from django.http import HttpResponse
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('http://127.0.0.1:80/invoice')
    return redirect('invoice:index')
