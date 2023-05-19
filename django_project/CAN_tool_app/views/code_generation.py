from CAN_tool_app.models import Car, CanBus, Message, Signal, UserMessageCheckboxes, UserSignalCheckboxes
from django.http import HttpResponse
from django.shortcuts import render, redirect
from io import BytesIO
from zipfile import ZipFile
from CAN_tool_app.views.code_generation_utils import signal_to_groups
from CAN_tool_app.views.h_code import generate_h_code
from CAN_tool_app.views.c_code import generate_c_code
from django.contrib import messages as popup_messages


def generate_code(car_id, can_bus_id, rx, tx, mc):
    mc = mc[0]
    can_bus = CanBus.objects.get(pk=can_bus_id)
    in_memory = BytesIO()
    both = []
    for message_id in tx:
        for signal_id in rx:
            signal = Signal.objects.get(pk=signal_id.split('-')[0])
            if signal.message.id == int(message_id):
                if message_id not in both:
                    both.append(message_id)
    rx_copy = rx.copy()
    for message_id in both:
        if message_id in tx:
            tx.remove(message_id)
        for signal_id in rx:
            signal = Signal.objects.get(pk=signal_id.split('-')[0])
            if signal.message.id == int(message_id):
                rx_copy.remove(str(signal_id))
    rx = rx_copy
    with ZipFile(in_memory, "w") as zip:
        zip.mkdir("Inc")
        zip.mkdir("Src")
        zip.writestr("Inc/CAN2023.h", generate_h_code(rx, tx, both))
        zip.writestr("Src/CAN2023.c", generate_c_code(mc, rx, tx + both))
    c = in_memory.getvalue()
    can_bus_name = can_bus.name.replace(" ", "_")
    response = HttpResponse(c, content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="' + can_bus_name + '.zip"'
    return response


def messages_selection(request, car_id, can_bus_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            tx = request.POST.getlist('messages_checkbox')
            rx = request.POST.getlist('signals_checkbox')
            mc = request.POST.getlist('microcontroller')
            return generate_code(car_id, can_bus_id, rx, tx, mc)

        car = Car.objects.get(pk=car_id)
        can_bus = CanBus.objects.get(pk=can_bus_id)

        messages = Message.objects.filter(can_bus_id=can_bus_id).order_by('identifier')
        for message in messages:
            signals = Signal.objects.filter(message_id=message.id).order_by('start_bit')
            if len(signals) > 0:
                last_signal = signals[len(signals) - 1]
                last_bit = last_signal.start_bit + last_signal.length
                msg_length = int(last_bit / 8) + (last_bit % 8 > 0)
                if msg_length > 8:
                    popup_messages.error(request,
                                         'Správa ' + message.name
                                         + ' má dĺžku ' + str(msg_length) + ' bytov. Zbernica nebola exportovaná.')
                    return redirect('messages', car_id=car_id, can_bus_id=can_bus_id)

            bit = 0
            for signal in signals:
                if signal.start_bit >= bit or signal.multiplexer_signal is not None:
                    bit = signal.start_bit + signal.length
                else:
                    popup_messages.error(request,
                                         'Signály v správe ' + message.name
                                         + ' sa prekrývajú. Zbernica nebola exportovaná.')
                    return redirect('messages', car_id=car_id, can_bus_id=can_bus_id)

        table_messages = Message.objects.filter(can_bus_id=can_bus_id).order_by('identifier').values()
        table_messages = table_messages
        messages = []

        for message_n, msg in enumerate(table_messages):
            msg_signals = []
            signals = Signal.objects.filter(message_id=msg['id']).order_by('start_bit').values()
            groups = signal_to_groups(signals)

            for u, group in enumerate(groups):
                count = ''
                if group['count'] != 1:
                    count = group['count']
                msg_signals.append({
                    'id': group['id'],
                    'name': group['name'],
                    'striped': (message_n + u) % 2 == 1,
                    'receivers': group['receivers'],
                    'ids': group['ids'],
                    'count': count
                })

            messages.append({
                'id': msg['id'],
                'name': msg['name'],
                'identifier': hex(msg['identifier']),
                'transmitter': msg['transmitter'],
		'receivers':msg['receivers'],
                'signals': msg_signals,
                'striped': message_n % 2 == 0})

        msg_checkboxes = list(
            UserMessageCheckboxes.objects.filter(user=request.user).values_list('message_id', flat=True))

        sig_checkboxes = list(
            UserSignalCheckboxes.objects.filter(user=request.user).values_list('signal_id', flat=True))
        context = {
            'message_checkboxes': msg_checkboxes,
            'signals_checkboxes': sig_checkboxes,
            'car': car,
            'can_bus': can_bus,
            'table_messages': enumerate(messages, start=1)
        }
        return render(request, 'code.html', context)
    return redirect('login')


def checkboxes(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message_id = request.POST.get('message_id')
            signal_id = request.POST.get('signal_id')
            multiple_signal_id = request.POST.get('multiple_signal_id')
            if message_id is not None:
                message = Message.objects.get(pk=message_id)
                if UserMessageCheckboxes.objects.filter(message=message).filter(user=request.user).exists():
                    UserMessageCheckboxes.objects.filter(message=message).filter(user=request.user).delete()
                else:
                    UserMessageCheckboxes.objects.create(message=message, user=request.user)
            if signal_id is not None:
                signal = Signal.objects.get(pk=signal_id)
                if UserSignalCheckboxes.objects.filter(signal=signal).filter(user=request.user).exists():
                    UserSignalCheckboxes.objects.filter(signal=signal).filter(user=request.user).delete()
                else:
                    UserSignalCheckboxes.objects.create(signal=signal, user=request.user)

            if multiple_signal_id is not None:
                signals = Signal.objects.filter(message_id=multiple_signal_id)
                if request.POST.get('checked') == 'true':
                    for signal in signals:
                        if not UserSignalCheckboxes.objects.filter(signal=signal).filter(user=request.user).exists():
                            UserSignalCheckboxes.objects.create(signal=signal, user=request.user)
                else:
                    for signal in signals:
                        if UserSignalCheckboxes.objects.filter(signal=signal).filter(user=request.user).exists():
                            UserSignalCheckboxes.objects.filter(signal=signal).filter(user=request.user).delete()

    return redirect('login')
