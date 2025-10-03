from fastapi import APIRouter

from server.server_controller import ServerController
from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest

server_router = APIRouter()

server_controller = ServerController()

@server_router.post("/get_country")
async def get_ip_country(request: CountryRequest) -> str:
    res = server_controller.get_country(request)
    if res.is_successful():
        return f"The country of ip {request.ip_address} is: {res.get_data()}"
    return f"Something went wrong when looking for the country of ip {request.ip_address}. The error is: {res.get_error_msg()}"

@server_router.get("/get_all_ip_in_country")
async def get_all_ips(request: AllIPsInCountryRequest):
    return {"message": request.country}

@server_router.get("/get_top_countries")
async def get_top_countries():
    return ["a", "b", "c", "d", "e"]
