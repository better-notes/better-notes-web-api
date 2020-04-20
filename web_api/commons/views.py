from typing import Any

import dacite
from aiohttp import web

from web_api.commons import values
from web_api.commons import msgpack


class StorableEntityView(web.View):
    """TODO:"""

    value_class: Any

    async def get_value(self) -> Any:
        value_class_is_set = self.value_class != values.Value
        assert value_class_is_set, 'You must specify dataclass for view.'

        data = msgpack.loads(await self.request.read())
        result = dacite.from_dict(data_class=self.value_class, data=data)
        return result
