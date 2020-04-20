from typing import Any

import dacite
from aiohttp import web

from web_api.commons import values
from web_api.commons import msgpack


class StorableEntityView(web.View):
    """TODO:"""

    value_class: Any

    def _dacite_from_dict(self, value: Any) -> Any:
        return dacite.from_dict(data_class=self.value_class, data=value)

    async def get_values(self) -> Any:
        value_class_is_set = self.value_class != values.Value
        assert value_class_is_set, 'You must specify dataclass for view.'

        data = msgpack.loads(await self.request.read())
        return list(map(self._dacite_from_dict, data))
