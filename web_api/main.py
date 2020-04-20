from aiohttp import web
from web_api.notes import views

import asyncio
import uvloop


def create_app(loop: asyncio.AbstractEventLoop) -> web.Application:
    app = web.Application(loop=loop)
    app.add_routes(views.routes)
    return app


if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    app = create_app(loop)

    web.run_app(app)
