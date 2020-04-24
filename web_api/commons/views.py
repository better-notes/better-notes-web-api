from typing import Any, Generic, List, Type, TypeVar, cast

import dacite.core
from aiohttp import web

from web_api.commons import msgpack, values

T = TypeVar('T', bound=values.Value)


class StorableEntityView(web.View, Generic[T]):
    """TODO:"""

    value_class: Type[T] = cast(Type[T], values.Value)

    def _dacite_from_dict(self, value: Any) -> T:
        return dacite.core.from_dict(data_class=self.value_class, data=value)

    async def get_values(self) -> List[T]:
        value_class_is_set = self.value_class != values.Value
        assert value_class_is_set, 'You must specify dataclass for view.'

        data = msgpack.loads(await self.request.read())
        return list(map(self._dacite_from_dict, data))
