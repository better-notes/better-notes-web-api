from aiohttp import web
from web_api.notes import views

import asyncio
import uvloop


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(views.routes)
    return app


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = create_app()

    web.run_app(app)
