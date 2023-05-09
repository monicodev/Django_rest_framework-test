from django.urls import path

from .views import list_or_create_charge_point, get_update_or_delete_charge_point

app_name = "charge_point"

urlpatterns = [
    path('charge_point/', list_or_create_charge_point, name='list_or_create_charge_point'),
    path('charge_point/<int:pk>/', get_update_or_delete_charge_point, name='get_update_or_delete_charge_point'),
]
