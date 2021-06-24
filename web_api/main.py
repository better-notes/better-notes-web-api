import uvicorn
import uvloop
from fastapi import FastAPI
from fastapi.routing import APIRouter
from pydantic.error_wrappers import ValidationError
from starlette.middleware.cors import CORSMiddleware

from web_api.accounts import views as accounts_views
from web_api.commons.exception_handlers import validation_error_exception_handler
from web_api.notes import views as notes_views
from web_api.settings import Settings


def include_api_v1_router(app: FastAPI, router: APIRouter, tags: list[str]) -> None:
    """Prefix all given routes with first version."""
    api_v1_prefix = '/api/v1'
    app.include_router(router, prefix=api_v1_prefix, tags=tags)


def get_application() -> FastAPI:
    app = FastAPI()
    include_api_v1_router(app, notes_views.router, tags=['Notes'])
    include_api_v1_router(app, accounts_views.router, tags=['Accounts'])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_exception_handler(
        ValidationError, validation_error_exception_handler,
    )

    return app


uvloop.install()
app = get_application()


if __name__ == '__main__':
    settings = Settings()
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
