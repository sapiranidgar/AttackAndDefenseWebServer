import logging
import httpx
from fastapi import APIRouter, Request, Response

from proxy.proxy_controller import ProxyController

logger = logging.getLogger(__name__)

DEFAULT_REQUEST_LIMIT = 5
DEFAULT_PATHS_LIMIT = 5
DEFAULT_TIME_WINDOW = 10
TARGET_URL = "http://127.0.0.1:8000"  # Local web server to forward requests to
AVAILABLE_REQUEST_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]

proxy_router = APIRouter()
proxy_controller = ProxyController.get_instance()



@proxy_router.api_route("/{path:path}", methods=AVAILABLE_REQUEST_METHODS)
async def proxy(request: Request, path: str):
    client_ip = request.client.host

    # if there is an attack with this ip
    if not proxy_controller.is_allowed(client_ip, path):
        logger.warning("Detected an attack by ip: {client_ip} and path: {path}".format(client_ip=client_ip, path=path))
        return Response(
            content="Request blocked by proxy: suspected attack.",
            status_code=403
        )

    # if not, forward request to the web server
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # Prepare the request to forward
        url = f"{TARGET_URL}/{path}"
        headers = dict(request.headers)
        body = await request.body()

        # Forward the request to target server
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body
        )
        logger.info("Forwarded message to server successfully.")
        # Return the target server's response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
