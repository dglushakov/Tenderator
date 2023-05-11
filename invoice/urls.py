from django.urls import path

from . import views

app_name = 'invoice'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('save/', views.save_invoice_to_csv, name='save_invoice_to_csv'),
    path('save/<str:categories_and_manufacturers>', views.save_invoice_to_csv, name='save_invoice_to_csv'),


]
