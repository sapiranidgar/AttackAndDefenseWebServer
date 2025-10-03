from fastapi import FastAPI
import uvicorn
from server_routes import server_router  # import your routes


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(server_router)
    return app


if __name__ == "__main__":
    app = create_app()  # only created when you run main.py
    uvicorn.run(app, host="127.0.0.1", port=8000)
