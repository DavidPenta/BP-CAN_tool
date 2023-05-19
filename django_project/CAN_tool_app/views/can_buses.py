from CAN_tool_app.models import Car, CanBus, UserPreferences
from CAN_tool_app.forms import CanBusForm
from django.shortcuts import render, redirect


def can_buses_table(request, car_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            col_name = request.POST.get('column_name')
            col_value = request.POST.get('column_value')
            user_preferences = UserPreferences.objects.filter(user=request.user.username)
            if col_value == 'hide':
                val = 1
            else:
                val = 0
            user_preferences.update(**{col_name: val})
        car = Car.objects.get(pk=car_id)
        table_can_buses = CanBus.objects.filter(car_id=car_id).order_by('changed_at')
        user_preferences = UserPreferences.objects.get(user=request.user.username)
        can_bus_preferences = {
            "can_bus_name": user_preferences.can_bus_name,
            "can_bus_note": user_preferences.can_bus_note,
            "can_bus_author": user_preferences.can_bus_author,
            "can_bus_changed_at": user_preferences.can_bus_changed_at,
            "can_bus_created_at": user_preferences.can_bus_created_at,
        }
        context = {'car': car, 'user_preferences': can_bus_preferences, 'table_can_buses': enumerate(table_can_buses, start=1)}
        return render(request, 'can-buses.html', context)

    return redirect('login')


def create_can_bus(request, car_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        if request.method == 'POST':
            form = CanBusForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                note = form.cleaned_data.get('note')
                if name is not None:
                    author = request.user.username
                    CanBus.objects.create(car=car, name=name, note=note, author=author)
                return redirect('can-buses', car_id=car_id)
        else:
            form = CanBusForm()

        context = {'car': car, 'form': form}
        return render(request, 'can-bus_create.html', context)
    return redirect('login')


def edit_can_buses(request, car_id, can_bus_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        can_bus = CanBus.objects.get(pk=can_bus_id)
        initial_data = {'name': can_bus.name, 'note': can_bus.note}
        form = CanBusForm(initial=initial_data)
        if request.method == 'POST':
            form = CanBusForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                note = form.cleaned_data.get('note')
                if name is not None and can_bus.name != name:
                    can_bus.name = name
                    can_bus.save()
                if can_bus.note != note:
                    can_bus.note = note
                    can_bus.save()
                return redirect('messages', car_id=car_id, can_bus_id=can_bus_id)
        context = {'car': car, 'can_bus': can_bus, 'form': form}
        return render(request, 'can-bus_edit.html', context)
    return redirect('login')


def delete_can_bus(request, car_id, can_bus_id):
    if request.user.is_authenticated:
        can_bus = CanBus.objects.get(pk=can_bus_id)
        can_bus.delete()
        return redirect('can-buses', car_id=car_id,)
    return redirect('login')
