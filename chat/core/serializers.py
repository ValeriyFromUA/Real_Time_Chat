from typing import Sequence


def serialize_operations_list(data_list: Sequence):
    return {
        'id': line[0],
        'quantity': line[1],
        'instrument_type': line[2],
        'data': line[3],
        'type': line[4]
    }
