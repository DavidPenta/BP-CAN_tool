from CAN_tool_app.forms import UploadDBCForm
from CAN_tool_app.models import Car, CanBus, Message, Signal
from django.http import HttpResponse
from django.shortcuts import render, redirect
import cantools
from django.contrib import messages as popup_messages


def save_dbc_to_db(car_id, name, note, author, file):
    str_text = ''
    car = Car.objects.get(pk=car_id)
    can_bus = CanBus.objects.create(
        car=car,
        name=name,
        note=note,
        author=author
    )

    for line in file:
        str_text = str_text + line.decode('cp1252')
    db = cantools.database.load_string(str_text)

    for msg in db.messages:

        transmitters = ""
        if msg.senders is not None:
            for transmitter in msg.senders:
                transmitters += transmitter + " "

        message = Message.objects.create(
            can_bus=can_bus,
            identifier=msg.frame_id,
            name=msg.name,
            note=msg.comment,
            transmitter=transmitters,
            receivers=None,
            author=author)

        msg_receivers = ""

        for signal in msg.signals:

            if signal.byte_order == 'little_endian':
                is_little_endian = True
            else:
                is_little_endian = False

            if signal.multiplexer_signal is not None:
                multiplexer_signal = Signal.objects.get(message=message, name=signal.multiplexer_signal)
            else:
                multiplexer_signal = None

            if signal.multiplexer_ids is not None:
                multiplexer_value = signal.multiplexer_ids[0]
            else:
                multiplexer_value = None

            receivers = ""
            if signal.receivers is not None:
                for receiver in signal.receivers:
                    receivers += receiver + " "
                    if receiver not in msg_receivers:
                        msg_receivers += receiver + " "

            Signal.objects.create(
                message=message,
                name=signal.name,
                start_bit=signal.start,
                length=signal.length,
                author=author,
                is_little_endian=is_little_endian,
                is_signed=signal.is_signed,
                factor=signal.scale,
                offset=signal.offset,
                min=signal.minimum,
                max=signal.maximum,
                unit=signal.unit,
                receivers=receivers,
                is_multiplexer=signal.is_multiplexer,
                multiplexer_signal=multiplexer_signal,
                multiplexer_value=multiplexer_value,
                note=signal.comment
            )

        if message.receivers != msg_receivers:
            message.receivers = msg_receivers
            message.save()


def import_dbc(request, car_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadDBCForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                note = form.cleaned_data.get('note')
                file = request.FILES['file']
                if name is not None and file is not None:
                    author = request.user.username
                    save_dbc_to_db(car_id, name, note, author, file)
                    return redirect('can-buses', car_id=car_id)

        car = Car.objects.get(pk=car_id)
        form = UploadDBCForm()
        return render(request, 'import_dbc.html', {'car': car, 'form': form})

    return redirect('login')


def export_dbc(request, car_id, can_bus_id):
    if request.user.is_authenticated:
        db = cantools.database.Database()
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

        for message in messages:
            signals = Signal.objects.filter(message_id=message.id).order_by('start_bit')
            signals_list = []
            length = 0
            start_bit = -1

            for signal in signals:
                if signal.start_bit > start_bit:
                    length += signal.length
                    start_bit = signal.start_bit

                if signal.is_little_endian:
                    byte_order = 'little_endian'
                else:
                    byte_order = 'big_endian'

                if signal.multiplexer_signal is not None:
                    multiplexer_signal = signal.multiplexer_signal.id
                else:
                    multiplexer_signal = None

                if signal.multiplexer_value is not None:
                    multiplexer_value = [signal.multiplexer_value]
                else:
                    multiplexer_value = None

                if signal.receivers == '':
                    receivers = None
                else:
                    receivers = signal.receivers.split()

                if signal.note == '':
                    note = None
                else:
                    note = signal.note

                if signal.factor.is_integer():
                    signal.factor = int(signal.factor)

                if signal.offset.is_integer():
                    signal.offset = int(signal.offset)

                if signal.min is not None and signal.min.is_integer():
                    signal.min = int(signal.min)

                if signal.max is not None and signal.max.is_integer():
                    signal.max = int(signal.max)

                signals_list.append(cantools.database.Signal(
                    name=signal.name,
                    start=signal.start_bit,
                    length=signal.length,
                    byte_order=byte_order,
                    is_signed=signal.is_signed,
                    scale=signal.factor,
                    offset=signal.offset,
                    minimum=signal.min,
                    maximum=signal.max,
                    unit=signal.unit,
                    receivers=receivers,
                    is_multiplexer=signal.is_multiplexer,
                    multiplexer_signal=multiplexer_signal,
                    multiplexer_ids=multiplexer_value,
                    comment=note)
                )

            if message.transmitter == '':
                transmitter = None
            else:
                transmitter = message.transmitter.split()

            signals = Signal.objects.filter(message_id=message).order_by('-start_bit')
            if len(signals) > 0:
                last_bit = signals[0].start_bit + signals[0].length
                msg_length = int(last_bit / 8) + (last_bit % 8 > 0)
            else:
                msg_length = 0

            if message.note == '':
                note = None
            else:
                note = message.note

            msg = cantools.database.Message(
                frame_id=message.identifier,
                name=message.name,
                comment=note,
                length=msg_length,
                senders=transmitter,
                signals=signals_list
            )

            db.messages.append(msg)

        db.refresh()
        can_bus = CanBus.objects.get(pk=can_bus_id)
        can_bus_name = can_bus.name.replace(" ", "_")

        file_data = db.as_dbc_string().encode('cp1252')
        response = HttpResponse(file_data, content_type='text/plain charset=cp1252')
        response['Content-Disposition'] = 'attachment; filename="' + can_bus_name + '.dbc"'
        return response
    return redirect('login')
