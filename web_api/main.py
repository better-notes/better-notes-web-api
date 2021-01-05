from fastapi.routing import APIRouter
import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from web_api.notes import views as notes_views
from web_api.accounts import views as accounts_views


def include_api_v1_router(
    app: FastAPI, router: APIRouter, tags: list[str],
) -> None:
    api_v1_prefix = '/api/v1'
    app.include_router(router, prefix=api_v1_prefix, tags=tags)


def get_application() -> FastAPI:
    app = FastAPI()
    include_api_v1_router(app, notes_views.router, tags=['Notes'])
    include_api_v1_router(app, accounts_views.router, tags=['Accounts'])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


uvloop.install()
app = get_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
