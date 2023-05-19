from CAN_tool_app.models import Car, CanBus, Message, UserPreferences, Signal
from CAN_tool_app.forms import MessageForm
from django.shortcuts import render, redirect


def messages_table(request, car_id, can_bus_id):
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
        can_bus = CanBus.objects.get(pk=can_bus_id)
        table_messages = Message.objects.filter(can_bus_id=can_bus_id).order_by('identifier')
        table_messages = table_messages.values()
        for msg in table_messages:
            msg['hex'] = format(msg['identifier'], 'x').upper()

            signals = Signal.objects.filter(message_id=msg['id']).order_by('-start_bit')

            if len(signals) > 0:
                last_bit = signals[0].start_bit + signals[0].length
                msg['length'] = int(last_bit / 8) + (last_bit % 8 > 0)
            else:
                msg['length'] = 0

        user_preferences = UserPreferences.objects.get(user=request.user.username)
        can_bus_preferences = {
            "message_id": user_preferences.message_id,
            "message_name": user_preferences.message_name,
            "message_length": user_preferences.message_length,
            "message_transmitter": user_preferences.message_transmitter,
            "message_receivers": user_preferences.message_receivers,
            "message_note": user_preferences.message_note,
            "message_author": user_preferences.message_author,
            "message_changed_at": user_preferences.message_changed_at,
            "message_created_at": user_preferences.message_created_at,
        }
        context = {'car': car, 'can_bus': can_bus, 'user_preferences': can_bus_preferences,
                   'table_messages': enumerate(table_messages, start=1)}
        return render(request, 'messages.html', context)

    return redirect('login')


def create_messages(request, car_id, can_bus_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        can_bus = CanBus.objects.get(pk=can_bus_id)
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                identifier = int(form.cleaned_data.get('identifier'), base=16)
                name = form.cleaned_data.get('name')
                transmitter = form.cleaned_data.get('transmitter')
                receivers = form.cleaned_data.get('receivers')
                note = form.cleaned_data.get('note')
                if name is not None and identifier is not None:
                    author = request.user.username
                    Message.objects.create(can_bus=can_bus,
                                           identifier=identifier,
                                           name=name,
                                           note=note,
                                           transmitter=transmitter,
                                           receivers=receivers,
                                           author=author)
                return redirect('messages', car_id=car_id, can_bus_id=can_bus_id)
        else:
            form = MessageForm()

        context = {'car': car, 'can_bus': can_bus, 'form': form}
        return render(request, 'messages_create.html', context)
    return redirect('login')


def edit_messages(request, car_id, can_bus_id, message_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        can_bus = CanBus.objects.get(pk=can_bus_id)
        message = Message.objects.get(pk=message_id)
        initial_data = {'identifier': format(message.identifier, 'x').upper(),
                        'name': message.name,
                        'note': message.note,
                        'receivers': message.receivers,
                        'transmitter': message.transmitter
                        }
        form = MessageForm(initial=initial_data)
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                identifier = int(form.cleaned_data.get('identifier'), base=16)
                name = form.cleaned_data.get('name')
                transmitter = form.cleaned_data.get('transmitter')
                receivers = form.cleaned_data.get('receivers')
                note = form.cleaned_data.get('note')
                if identifier is not None and message.identifier != identifier:
                    message.identifier = identifier
                    message.save()
                if name is not None and message.name != name:
                    message.name = name
                    message.save()
                if message.note != note:
                    message.note = note
                    message.save()
                if message.transmitter != transmitter:
                    message.transmitter = transmitter
                    message.save()
                if message.receivers != receivers:
                    message.receivers = receivers
                    message.save()
                return redirect('signals', car_id=car_id, can_bus_id=can_bus_id, message_id=message_id)
        context = {'car': car, 'can_bus': can_bus, 'message': message, 'form': form}
        return render(request, 'messages_edit.html', context)
    return redirect('login')


def delete_messages(request, car_id, can_bus_id, message_id):
    if request.user.is_authenticated:
        message = Message.objects.get(pk=message_id)
        message.delete()
        return redirect('messages', car_id=car_id, can_bus_id=can_bus_id)
    return redirect('login')
