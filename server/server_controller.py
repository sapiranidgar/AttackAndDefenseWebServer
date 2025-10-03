from fastapi import APIRouter
from server.server_requests.country_request import CountryRequest

server_router = APIRouter()

@server_router.post("/get_country")
async def get_ip_country(request: CountryRequest):
    return {"message": request.ip_address}
