import logging
import httpx
from fastapi import APIRouter, Request, Response

logger = logging.getLogger(__name__)
proxy_router = APIRouter()
TARGET_URL = "http://127.0.0.1:8000"  # Local web server to forward requests to
AVAILABLE_REQUEST_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


@proxy_router.api_route("/{path:path}", methods=AVAILABLE_REQUEST_METHODS)
async def proxy(request: Request, path: str):
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

        # Return the target server's response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
