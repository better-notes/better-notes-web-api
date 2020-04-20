import datetime
from typing import Any

import bson
import funcy
import msgpack


def decode(obj: Any) -> Any:
    if '__datetime__' in obj:
        return datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    if '__object_id__' in obj:
        return bson.ObjectId(obj['as_str'])
    return obj


def encode(obj: Any) -> Any:
    if isinstance(obj, datetime.datetime):
        return {
            '__datetime__': True,
            'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f"),
        }
    if isinstance(obj, bson.ObjectId):
        return {'__object_id__': True, 'as_str': str(obj)}
    return obj


loads = funcy.partial(msgpack.loads, object_hook=decode)
dumps = funcy.partial(msgpack.dumps, default=encode)
