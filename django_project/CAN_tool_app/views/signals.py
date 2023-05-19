from CAN_tool_app.models import Car, CanBus, Message, Signal, UserPreferences
from CAN_tool_app.forms import SignalForm
from django.shortcuts import render, redirect


def signals_table(request, car_id, can_bus_id, message_id):
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
        message = Message.objects.get(pk=message_id)

        table_signals = Signal.objects.filter(message_id=message_id).order_by('start_bit')
        for signal in table_signals:
            if signal.is_signed:
                signal.is_signed = 'signed'
            else:
                signal.is_signed = 'unsigned'

            if signal.is_little_endian:
                signal.is_little_endian = 'Intel - little-endian'
            else:
                signal.is_little_endian = 'Motorola - big-endian'

            if signal.factor.is_integer():
                signal.factor = int(signal.factor)

            if signal.offset.is_integer():
                signal.offset = int(signal.offset)

            if signal.min is not None and signal.min.is_integer():
                signal.min = int(signal.min)

            if signal.max is not None and signal.max.is_integer():
                signal.max = int(signal.max)

        user_preferences = UserPreferences.objects.get(user=request.user.username)

        signal_preferences = {
            "signal_name": user_preferences.signal_name,
            "signal_start_bit": user_preferences.signal_start_bit,
            "signal_length": user_preferences.signal_length,
            "signal_is_little_endian": user_preferences.signal_is_little_endian,
            "signal_is_signed": user_preferences.signal_is_signed,
            "signal_factor": user_preferences.signal_factor,
            "signal_offset": user_preferences.signal_offset,
            "signal_min": user_preferences.signal_min,
            "signal_max": user_preferences.signal_max,
            "signal_unit": user_preferences.signal_unit,
            "signal_receivers": user_preferences.signal_receivers,
            "signal_is_multiplexer": user_preferences.signal_is_multiplexer,
            "signal_multiplexer_signal": user_preferences.signal_multiplexer_signal,
            "signal_multiplexer_value": user_preferences.signal_multiplexer_value,
            "signal_note": user_preferences.signal_note,
            "signal_author": user_preferences.signal_author,
            "signal_changed_at": user_preferences.signal_changed_at,
            "signal_created_at": user_preferences.signal_created_at
        }
        context = {'car': car, 'can_bus': can_bus, 'message': message, 'user_preferences': signal_preferences,
                   'table_signals': enumerate(table_signals, start=1)}
        return render(request, 'signals.html', context)

    return redirect('login')


def create_signals(request, car_id, can_bus_id, message_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        can_bus = CanBus.objects.get(pk=can_bus_id)
        message = Message.objects.get(pk=message_id)
        if request.method == 'POST':
            form = SignalForm(request.POST, message_id=message_id)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                length = form.cleaned_data.get('length')
                start_bit = form.cleaned_data.get('start_bit')
                is_little_endian = form.cleaned_data.get('is_little_endian')
                is_signed = form.cleaned_data.get('is_signed')
                factor = form.cleaned_data.get('factor')
                offset = form.cleaned_data.get('offset')
                min = form.cleaned_data.get('min')
                max = form.cleaned_data.get('max')
                unit = form.cleaned_data.get('unit')
                receivers = form.cleaned_data.get('receivers')
                is_multiplexer = form.cleaned_data.get('is_multiplexer')
                multiplexer_signal = form.cleaned_data.get('multiplexer_signal')
                multiplexer_value = form.cleaned_data.get('multiplexer_value')
                note = form.cleaned_data.get('note')

                if name is not None and length is not None and start_bit is not None:
                    author = request.user.username
                    Signal.objects.create(
                        message=message,
                        name=name,
                        length=length,
                        author=author,
                        start_bit=start_bit,
                        note=note,
                        is_little_endian=is_little_endian,
                        is_signed=is_signed,
                        factor=factor,
                        offset=offset,
                        min=min,
                        max=max,
                        unit=unit,
                        receivers=receivers,
                        is_multiplexer=is_multiplexer,
                        multiplexer_signal=multiplexer_signal,
                        multiplexer_value=multiplexer_value)
                return redirect('signals', car_id=car_id, can_bus_id=can_bus_id, message_id=message_id)
        else:
            initial_data = {'factor': 1,
                            'offset': 0,
                            }
            form = SignalForm(initial=initial_data, message_id=message_id)

        context = {'car': car, 'message': message, 'can_bus': can_bus, 'form': form}
        return render(request, 'signals_create.html', context)
    return redirect('login')


def edit_signals(request, car_id, can_bus_id, message_id, signal_id):
    if request.user.is_authenticated:
        car = Car.objects.get(pk=car_id)
        can_bus = CanBus.objects.get(pk=can_bus_id)
        message = Message.objects.get(pk=message_id)
        signal = Signal.objects.get(pk=signal_id)
        initial_data = {'name': signal.name,
                        'start_bit': signal.start_bit,
                        'length': signal.length,
                        'is_little_endian': signal.is_little_endian,
                        'is_signed': signal.is_signed,
                        'factor': signal.factor,
                        'offset': signal.offset,
                        'min': signal.min,
                        'max': signal.max,
                        'unit': signal.unit,
                        'receivers': signal.receivers,
                        'is_multiplexer': signal.is_multiplexer,
                        'multiplexer_signal': signal.multiplexer_signal,
                        'multiplexer_value': signal.multiplexer_value,
                        'note': signal.note,
                        'author': signal.author,
                        }
        form = SignalForm(initial=initial_data, message_id=message_id)
        if request.method == 'POST':
            form = SignalForm(request.POST, message_id=message_id)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                start_bit = form.cleaned_data.get('start_bit')
                length = form.cleaned_data.get('length')

                if name is not None and start_bit is not None and length is not None:
                    signal.name = name
                    signal.start_bit = start_bit
                    signal.length = length
                    signal.is_little_endian = form.cleaned_data.get('is_little_endian')
                    signal.is_signed = form.cleaned_data.get('is_signed')
                    signal.factor = form.cleaned_data.get('factor')
                    signal.offset = form.cleaned_data.get('offset')
                    signal.min = form.cleaned_data.get('min')
                    signal.max = form.cleaned_data.get('max')
                    signal.unit = form.cleaned_data.get('unit')
                    signal.receivers = form.cleaned_data.get('receivers')
                    signal.is_multiplexer = form.cleaned_data.get('is_multiplexer')
                    signal.multiplexer_signal = form.cleaned_data.get('multiplexer_signal')
                    signal.multiplexer_value = form.cleaned_data.get('multiplexer_value')
                    signal.note = form.cleaned_data.get('note')
                    signal.save()

                return redirect('signals', car_id=car_id, can_bus_id=can_bus_id, message_id=message_id)
        context = {'car': car, 'can_bus': can_bus, 'message': message, 'signal': signal, 'form': form}
        return render(request, 'signals_edit.html', context)
    return redirect('login')


def delete_signals(request, car_id, can_bus_id, message_id, signal_id):
    if request.user.is_authenticated:
        signal = Signal.objects.get(pk=signal_id)
        signal.delete()
        return redirect('signals', car_id=car_id, can_bus_id=can_bus_id, message_id=message_id)
    return redirect('login')
