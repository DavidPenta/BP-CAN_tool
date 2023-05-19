from CAN_tool_app.models import Car, UserPreferences
from CAN_tool_app.forms import CarForm
from django.shortcuts import render, redirect
from django.db.models import F


def cars_table(request):
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
        table_cars = Car.objects.all().order_by(F('year').desc(nulls_last=True))
        user_preferences = UserPreferences.objects.get(user=request.user.username)
        car_preferences = {
            "car_name": user_preferences.car_name,
            "car_year": user_preferences.car_year,
            "car_note": user_preferences.car_note,
            "car_author": user_preferences.car_author,
            "car_changed_at": user_preferences.car_changed_at,
            "car_created_at": user_preferences.car_created_at,
        }
        context = {'user_preferences': car_preferences, 'table_cars': enumerate(table_cars, start=1)}
        return render(request, 'cars.html', context)
    return redirect('login')


def create_car(request):
    if request.user.is_authenticated:
        form = CarForm()
        if request.method == 'POST':
            form = CarForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                year = form.cleaned_data.get('year')
                note = form.cleaned_data.get('note')
                if name is not None:
                    author = request.user.username
                    Car.objects.create(name=name, year=year, note=note, author=author)
                return redirect('cars')
        context = {'form': form}
        return render(request, 'car_create.html', context)
    return redirect('login')


def delete_car(request, car_id):
    if request.user.is_authenticated:
        car = Car.objects.get(id=car_id)
        car.delete()
        return redirect('cars')
    return redirect('login')


def edit_car(request, car_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        initial_data = {
            'name': car.name,
            'year': car.year,
            'note': car.note
        }
        form = CarForm(initial=initial_data)
        if request.method == 'POST':
            form = CarForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                year = form.cleaned_data.get('year')
                note = form.cleaned_data.get('note')
                if name is not None and car.name != name:
                    car.name = name
                    car.save()
                if car.year != year:
                    car.year = year
                    car.save()
                if car.note != note:
                    car.note = note
                    car.save()
                return redirect('can-buses', car_id=car_id)
        context = {'car': car, 'form': form}
        return render(request, 'car_edit.html', context)
    return redirect('login')
