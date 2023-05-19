from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('post/checkboxes/', views.checkboxes, name="checkboxes"),
    path('cars/', views.cars_table, name='cars'),
    path('cars/create/', views.create_car, name='cars_create'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='cars_delete'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='cars_edit'),
    path('cars/<int:car_id>/can-buses/', views.can_buses_table, name='can-buses'),
    path('cars/<int:car_id>/can-buses/create/', views.create_can_bus, name='can-buses_create'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/delete/', views.delete_can_bus, name='can_bus_delete'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/edit/', views.edit_can_buses, name='can-buses_edit'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/', views.messages_table, name='messages'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/create/', views.create_messages, name='messages_create'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/<int:message_id>/delete/', views.delete_messages, name='messages_delete'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/<int:message_id>/edit/', views.edit_messages, name='messages_edit'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/<int:message_id>/signals/', views.signals_table, name='signals'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/<int:message_id>/signals/create/', views.create_signals, name='signals_create'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/<int:message_id>/signals/<int:signal_id>/delete/', views.delete_signals, name='signals_delete'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/messages/<int:message_id>/signals/<int:signal_id>/edit/', views.edit_signals, name='signals_edit'),
    path('cars/<int:car_id>/import_dbc/', views.import_dbc, name='import_dbc'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/export_dbc/', views.export_dbc, name='export_dbc'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/c_code/', views.messages_selection, name='messages_selection'),
    path('cars/<int:car_id>/can-buses/<int:can_bus_id>/c_code/<int:type>/', views.generate_code, name='code'),
]
