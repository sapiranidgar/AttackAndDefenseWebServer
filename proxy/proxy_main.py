import threading

from fastapi import FastAPI
import uvicorn

from proxy.attack_monitor import start_attack_monitor
from proxy.proxy_routes import proxy_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(proxy_router)
    return app


if __name__ == "__main__":
    monitor_thread = threading.Thread(target=start_attack_monitor, daemon=True)
    monitor_thread.start()

    app = create_app()  # only created when you run main.py
    uvicorn.run(app, host="127.0.0.1", port=8001)
