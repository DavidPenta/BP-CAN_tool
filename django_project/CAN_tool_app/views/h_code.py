from CAN_tool_app.models import Message, Signal
from datetime import datetime
from CAN_tool_app.views.code_generation_utils import signal_to_groups, get_type


def generate_message_comment(message, groups):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    h_code = ""

    signals = Signal.objects.filter(message_id=message).order_by('-start_bit')
    if len(signals) > 0:
        last_bit = signals[0].start_bit + signals[0].length
        msg_length = int(last_bit / 8) + (last_bit % 8 > 0)
    else:
        msg_length = 0

    if message.note is None:
        message.note = ""

    h_code += '#define ID_' + message.name + ' ' + str(hex(message.identifier)) + '\n\
#define DLC_' + message.name + ' ' + str(msg_length) + '\n\
/* ' + message.name + '\n\
 * ' + str(message.note) + '\n\
 *\n\
 * ID ' + str(hex(message.identifier)) + '\n\
 * Message size DLC: ' + str(msg_length) + ' bytes\n\
 * Message is sent by node: ' + message.transmitter + '\n\
 * Message contains:\n\
 *                                  rep start len   type       comment\n'

    letter_num = 0
    table = []
    for signal in groups:
        if signal['note'] is None:
            signal['note'] = ""

        while len(table) < signal['start_bit']:
            table.append(' ')
        for j in range(signal['length']):
            table.append(alphabet[letter_num])
        letter_num += 1

        h_code += ' * ' + "{:<32}".format(signal['name']) + \
                  ' | ' + alphabet[letter_num - 1] + \
                  ' | ' + "{:<2}".format(str(signal['start_bit'])) + \
                  ' | ' + "{:<2}".format(str(signal['length'])) + \
                  ' | ' + "{:<8}".format(get_type(signal['length'], signal['is_signed'])) + \
                  ' | ' + signal['note'] + \
                  '\n'
    h_code += ' *\n *             bit\n\
 *     |7|6|5|4|3|2|1|0|\n'

    b = [' ', ' ', 'b', 'y', 't', 'e', ' ', ' ']
    table = table[:64] + [' '] * (64 - len(table))
    table = [table[i:i + 8] for i in range(0, len(table), 8)]
    for i in range(len(table)):
        table[i].insert(0, str(i))

    h_code += ' *  ' + '|\n *  '.join(
        [str(b[u] + ' ') + '|'.join([item for item in row]) for u, row in enumerate(table)]) + '\
|\n*/\ntypedef struct\n{\n'
    for signal in groups:
        h_code += '    ' + get_type(signal['length'], signal['is_signed']) + ' ' + str(signal['name']) + ';\n'
    h_code += '} ' + str(message.name) + '_TypeDef;\n\n'
    return h_code


def generate_h_code_tx(tx):
    h_code = ""
    for message_id in tx:
        message = Message.objects.get(pk=message_id)
        signals = Signal.objects.filter(message_id=message.id).order_by('start_bit')
        groups = signal_to_groups(signals.values())

        h_code += '#define Tx_' + message.name + ' 1\n//#define Rx_' + message.name + ' 1\n'
        h_code += generate_message_comment(message, groups)
        h_code += '#ifdef Tx_' + message.name + '\n\
void Tx_' + message.name + '_Data(CAN_HandleTypeDef* hcan, ' + message.name + '_TypeDef* ' + message.name + '_Data);\n\
#endif\n\n'

    return h_code


def generate_h_code_rx(rx):
    h_code = ""
    messages = {}
    for signal_id in rx:
        signal = Signal.objects.get(pk=signal_id.split('-')[0])
        message = signal.message.id
        if message not in messages:
            messages[message] = []

        if '-' in signal_id:
            mul_signal_ids = signal_id.split('-')
            for mul_signal_id in mul_signal_ids:
                mul_signal = Signal.objects.get(pk=mul_signal_id)
                messages[message].append(mul_signal.__dict__)
        else:
            signal = Signal.objects.get(pk=signal_id)
            messages[message].append(signal.__dict__)

    for message_id in messages:
        message = Message.objects.get(pk=message_id)
        groups = signal_to_groups(messages[message_id])
        h_code += '//#define Tx_' + message.name + ' 1\n#define Rx_' + message.name + ' 1\n'
        h_code += generate_message_comment(message, groups)
        h_code += '#ifdef Rx_' + message.name + '\n\
void Rx_' + message.name + '_Data(CAN_HandleTypeDef* hcan, ' + message.name + '_TypeDef* ' + message.name + '_Data);\n\
#endif\n\n'

    return h_code


def generate_h_code_both(tx):  # if message is both rx and tx
    h_code = ""
    for message_id in tx:
        message = Message.objects.get(pk=message_id)
        signals = Signal.objects.filter(message_id=message.id).order_by('start_bit')
        groups = signal_to_groups(signals.values())

        h_code += '#define Tx_' + message.name + ' 1\n#define Rx_' + message.name + ' 1\n'
        h_code += generate_message_comment(message, groups)
        h_code += '#ifdef Tx_' + message.name + '\n\
void Tx_' + message.name + '_Data(CAN_HandleTypeDef* hcan, ' + message.name + '_TypeDef* ' + message.name + '_Data);\n\
#endif\n\n'

    return h_code


def generate_h_code(rx, tx, both):
    today = datetime.today().strftime('%Y-%m-%d')
    h_code = '/**\n\
  ******************************************************************************\n\
  * @file    CAN2023.h\n\
  * @author  SGT Generated by tool\n\
  * @version V0.2.0 (generator)\n\
  * @date    ' + today + '\n\
  * @brief   CAN protocol application/PROFILE layer for use in SGT formula student electric 2023\n\
  ******************************************************************************\n\
    Header contains all CAN bus message structures and defines of signals\n\
  ******************************************************************************\n\
  Do not change document and messages structure!\n\n\
  HOW TO RECEIVE:\n\
  -do your init of CAN device in main.c\n\
  -define used structures by uncommenting in CAN2023.h\n\
  -use extern for CAN2023.h data structures in your main.c file\n\
  -send messages using declared functions. Received structures are saved automatically in receive structures\n\
  -work with data from structure :)\n\n\
  HOW TO TRANSMIT:\n\
  -fill structure of message you want to send\n\
  -call correspondent transmit function which will fill the TX message structure and transmit\n\
  ******************************************************************************\n*/\n\
#ifndef CAN2023_H_\n\
#define CAN2023_H_\n\n'

    h_code += generate_h_code_tx(tx)
    h_code += generate_h_code_rx(rx)
    h_code += generate_h_code_both(both)
    h_code += '#endif /* CAN2018_H_ */'

    return h_code
