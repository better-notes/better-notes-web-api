import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from web_api.notes import views


def get_application() -> FastAPI:
    uvloop.install()

    app = FastAPI()
    app.include_router(views.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
