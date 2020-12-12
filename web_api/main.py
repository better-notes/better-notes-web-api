import uvicorn
import uvloop
from fastapi import FastAPI

from web_api.notes import views


def get_application() -> FastAPI:
    uvloop.install()

    app = FastAPI()
    app.include_router(views.router)

    return app


app = get_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
