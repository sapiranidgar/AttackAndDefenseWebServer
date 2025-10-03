from fastapi import APIRouter

from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest

server_router = APIRouter()

@server_router.post("/get_country")
async def get_ip_country(request: CountryRequest):
    return {"message": request.ip_address}

@server_router.get("/get_all_ip_in_country")
async def get_all_ips(request: AllIPsInCountryRequest):
    return {"message": request.country}

@server_router.get("/get_top_countries")
async def get_top_countries():
    return ["a", "b", "c", "d", "e"]
