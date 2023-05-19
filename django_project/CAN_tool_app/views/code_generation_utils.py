def get_type(length, is_signed):
    c_type = ""

    if not is_signed:
        c_type += 'u'
    c_type += 'int'
    if length <= 8:
        c_type += '8'
    elif length <= 16:
        c_type += '16'
    elif length <= 32:
        c_type += '32'
    elif length <= 64:
        c_type += '64'
    c_type += '_t'

    return c_type


def signal_to_groups(signals):
    groups = []
    for sig in signals:
        group_i = -1
        for i in range(len(groups)):
            if sig['start_bit'] == groups[i]['start_bit'] and sig['multiplexer_signal_id'] == groups[i]['mul']:
                group_i = i
                break
        if group_i == -1:
            groups.append({
                'start_bit': sig['start_bit'],
                'mul': sig['multiplexer_signal_id'],
                'name': sig['name'],
                'id': sig['id'],
                'receivers': sig['receivers'],
                'length': sig['length'],
                'is_signed': sig['is_signed'],
                'note': sig['note'],
                'ids': str(sig['id']),
                'count': 1
            })

        else:
            name = groups[group_i]['name']
            length = len(name)
            if length < len(sig['name']):
                length = len(sig['name'])
            new_name = ''
            for j in range(length):
                if name[j] == sig['name'][j]:
                    new_name += name[j]
                else:
                    if len(new_name) > 1 and new_name[-1] == '0':
                        new_name = new_name[:-1] + 'X'
                    new_name += 'X'

            groups[group_i]['name'] = new_name
            groups[group_i]['ids'] += '-' + str(sig['id'])
            groups[group_i]['count'] += 1
    return groups
