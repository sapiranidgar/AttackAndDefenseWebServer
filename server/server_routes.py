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

@server_router.post("/get_all_ip_in_country")
async def get_all_ips(request: AllIPsInCountryRequest) -> str:
    res = server_controller.get_all_ips(request)
    if res.is_successful():
        return f"Here are all of the ip addresses in the country {request.country}: {res.get_data()}"
    return f"Something went wrong when looking for the ip's of {request.country}. The error is: {res.get_error_msg()}"


@server_router.get("/get_top_countries")
async def get_top_countries():
    res = server_controller.get_top_countries()
    if res.is_successful():
        data = res.get_data()
        return f"Here are the top {len(data)} countries: {data}"
    return f"Something went wrong when looking for top 5 countries. The error is: {res.get_error_msg()}"

