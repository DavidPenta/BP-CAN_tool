from CAN_tool_app.models import Message, Signal
from datetime import datetime
from CAN_tool_app.views.code_generation_utils import signal_to_groups, get_type


def signals_to_bytes(message, signals):
    c_code = ''
    byte_i = 0
    signal_i = 0
    signal_left_size = None
    signal_size = None
    name = None
    start_bit = None
    byte_left_size = 8
    last_signal_i = -1
    last_data_i = -1
    signals_count = len(signals)

    while signal_i < signals_count:
        if last_signal_i != signal_i:
            signal = signals[signal_i]
            start_bit = signal['start_bit']
            length = signal['length']
            name = signal['name']
            signal_size = length
            signal_left_size = length

        next_bit_start = byte_i * 8 + (8 - byte_left_size)
        if start_bit > next_bit_start:
            n = start_bit - next_bit_start
            byte_left_size -= n
            if byte_left_size <= 0:
                while byte_left_size <= 0:
                    byte_i += 1
                    byte_left_size += 8

        tmp_byte_left_size = byte_left_size
        byte_left_size -= signal_left_size
        signal_left_size -= tmp_byte_left_size
        mask_needed = signal_size + byte_left_size > 0
        row = '    TxData[' + str(byte_i) + '] '

        if last_data_i == byte_i:
            row += '|'

        row += '= (uint8_t)('

        if mask_needed:
            row += '('

        row += str(message.name) + '_Data->' + str(name)

        if byte_left_size > 0:
            row += ' << ' + str(byte_left_size)
        elif byte_left_size < 0:
            row += ' >> ' + str(byte_left_size * -1)

        if mask_needed:
            row += ')&0b'
            for i in range(signal_size + byte_left_size):
                row += '1'

        row += ');\n'

        last_signal_i = signal_i
        last_data_i = byte_i

        if signal_left_size <= 0:
            signal_i += 1

        if byte_left_size <= 0:
            byte_i += 1
            byte_left_size = 8

        c_code += row

    return c_code


def bytes_to_signals(message, signals):
    c_code = ''
    byte_i = 0
    signal_i = 0
    signal_left_size = None
    signal_size = None
    row = None
    byte_left_size = 8
    last_signal_i = -1
    signals_count = len(signals)

    while signal_i < signals_count:
        if last_signal_i != signal_i:
            signal = signals[signal_i]
            start_bit = signal['start_bit']
            length = signal['length']
            name = signal['name']
            is_signed = signal['is_signed']

            next_bit_start = byte_i * 8 + (8 - byte_left_size)
            if start_bit > next_bit_start:
                n = start_bit - next_bit_start
                byte_left_size -= n
                if byte_left_size <= 0:
                    while byte_left_size <= 0:
                        byte_i += 1
                        byte_left_size += 8

            row = '    ' + message.name + '_Data->' + name + ' = (' + get_type(length, is_signed) + ')('

            signal_size = length
            signal_left_size = length

        else:
            row += ' | '

        tmp_byte_left_size = byte_left_size
        byte_left_size -= signal_left_size
        signal_left_size -= tmp_byte_left_size
        mask_needed = signal_size + byte_left_size > 0

        if mask_needed:
            row += '('

        if byte_left_size != 0:
            row += '('

        row += 'RxData[' + str(byte_i) + ']'

        if mask_needed:
            row += '&0b'
            for i in range(signal_size + byte_left_size):
                row += '1'

        if byte_left_size > 0:
            row += ') >> ' + str(byte_left_size)
        elif byte_left_size < 0:
            row += ') << ' + str(byte_left_size * -1)

        if mask_needed:
            row += ')'

        last_signal_i = signal_i

        if signal_left_size <= 0:
            signal_i += 1

        if byte_left_size <= 0:
            byte_i += 1
            byte_left_size = 8

        if last_signal_i != signal_i:
            c_code += row + ');\n'

    return c_code


def generate_functions(message, groups):
    c_code = "\n\n"
    c_code += '#if defined(Tx_' + message.name + ') || defined(Rx_' + message.name + ')\n\
    ' + message.name + '_TypeDef ' + message.name + '_Data = {\n        '
    fields_rows = []
    for signal in groups:
        fields_rows.append('.' + signal['name'] + " = 0")
    c_code += ',\n        '.join(fields_rows)
    c_code += '\n   };\n#endif\n\n'
    c_code += '#ifdef Tx_' + message.name + '\n\
void Tx_' + message.name + '_Data(CAN_HandleTypeDef* hcan, ' + message.name + '_TypeDef* ' + message.name + '_Data)\n{\n\
    TxHeader.StdId = ID_' + message.name + ';\n\
    TxHeader.DLC = DLC_' + message.name + ';\n\
    TxHeader.ExtId = 0x0;\n\
    TxHeader.RTR = CAN_RTR_DATA;\n\
    TxHeader.IDE = CAN_ID_STD;\n\n'

    c_code += signals_to_bytes(message, groups)

    c_code += '\n    HAL_CAN_ActivateNotification(hcan,0xff);\n\
    HAL_CAN_AddTxMessage(hcan, &TxHeader, TxData, &TxMailbox);\n\
    HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData);\n\
}\n\
#endif\n\
#ifdef Rx_' + message.name + '\n\
void Rx_' + message.name + '_Data(CAN_HandleTypeDef* hcan, ' + message.name + '_TypeDef* ' + message.name + '_Data)\n\
{\n'
    c_code += bytes_to_signals(message, groups)
    c_code += '}\n#endif\n'
    return c_code


def generate_functions_tx(tx):
    c_code = ""
    for message_id in tx:
        message = Message.objects.get(pk=message_id)
        signals = Signal.objects.filter(message_id=message_id).order_by('start_bit')
        groups = signal_to_groups(signals.values())
        c_code += generate_functions(message, groups)
    return c_code


def generate_functions_rx(rx):
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
    c_code = ""
    for message_id in messages:
        message = Message.objects.get(pk=message_id)
        groups = signal_to_groups(messages[message_id])
        c_code += generate_functions(message, groups)
    return c_code


def generate_callback_tx(tx):
    c_code = ""
    for message_id in tx:
        message = Message.objects.get(pk=message_id)
        c_code += '#ifdef Rx_' + message.name + '\n        case ID_' + message.name + ':\n\
            Rx_' + message.name + '_Data(hcan, &' + message.name + '_Data);\n            break;\n#endif\n\n'
    return c_code


def generate_callback_rx(rx):
    c_code = ""
    messages = []
    for signal_id in rx:
        signal = Signal.objects.get(pk=signal_id.split('-')[0])
        message = signal.message.id
        if message not in messages:
            messages.append(message)
    for message_id in messages:
        message = Message.objects.get(pk=message_id)
        c_code += '#ifdef Rx_' + message.name + '\n        case ID_' + message.name + ':\n\
            Rx_' + message.name + '_Data(hcan, &' + message.name + '_Data);\n            break;\n#endif\n\n'
    return c_code


def generate_c_code(mc, rx, tx):
    today = datetime.today().strftime('%Y-%m-%d')
    c_code = '/**\n\
  ******************************************************************************\n\
  * @file    CAN2023.c\n\
  * @author  SGT Generated by tool\n\
  * @version V0.2.0 (generator)\n\
  * @date    ' + today + '\n\
  * @brief   CAN protocol application/PROFILE layer for use in SGT formula student electric 2023\n\
  ******************************************************************************\n\
*/\n\
#include \"stm32f' + str(mc) + 'xx_hal.h\"\n\
#include \"CAN2023.h\"\n\
#include \"main.h\"\n\
CAN_TxHeaderTypeDef TxHeader;\n\
CAN_RxHeaderTypeDef RxHeader;\n\
uint8_t TxData[8];\n\
uint8_t RxData[8];\n\
uint32_t TxMailbox;\n'

    c_code += generate_functions_tx(tx)
    c_code += generate_functions_rx(rx)

    c_code += '\n/** \\brief Zmaze CAN error ak je\n\
 *\n\
 * \\param hcan CAN_HandleTypeDef*\n\
 * \\return void\n\
 *\n\
 */\n\n\
void HAL_CAN_ErrorCallback(CAN_HandleTypeDef *hcan)\n\
{\n\
    hcan->ErrorCode = HAL_CAN_ERROR_NONE;\n\
    hcan->Instance->MSR &= 0x1C;\n\
}\n\
/**\n\
* @brief Event for CAN Rx message\n\
* @param Can controller message structure\n\
*/\n\
void HAL_CAN_RxCpltCallback(CAN_HandleTypeDef *hcan)\n\
{\n\
    switch (RxHeader.StdId)\n\
    {\n\n'
    c_code += generate_callback_tx(tx)
    c_code += generate_callback_rx(rx)
    c_code += '        default:\n\
            break;\n\
    }\n\
  HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData);\n\n\
  static uint8_t blink;\n\n\
  if(!(blink%10))\n\
  {\n\
      HAL_GPIO_TogglePin(CAN_LED_GPIO_Port, CAN_LED_Pin);\n\
  }\n\
  blink++;\n\
}\n\n\
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef* hcan)\n\
{\n\
    HAL_CAN_RxCpltCallback(hcan);\n}'

    return c_code
