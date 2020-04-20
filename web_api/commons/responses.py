from typing import Any

from aiohttp import web
from web_api.commons import msgpack


class MSGPackResponse(web.Response):
    def __init__(self, *, data: Any, **kwargs: Any) -> None:
        assert not kwargs.get('body') and not kwargs.get('text')
        super().__init__(body=msgpack.dumps(data), **kwargs)
