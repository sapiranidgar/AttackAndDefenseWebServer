import logging

from fastapi import APIRouter

from server.server_controller import ServerController
from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest

logger = logging.getLogger(__name__)
server_router = APIRouter()

server_controller = ServerController.get_instance()

@server_router.post("/get_country")
async def get_ip_country(request: CountryRequest) -> str:
    logger.info("User sent post request for geolocation.")
    res = server_controller.get_country(request)
    if res.is_successful():
        logger.info("User received an answer for geolocation.")
        return f"The country of ip {request.ip_address} is: {res.get_data()}"
    logger.info("User received a failed answer for geolocation.")
    return f"Something went wrong when looking for the country of ip {request.ip_address}. The error is: {res.get_error_msg()}"

@server_router.post("/get_all_ip_in_country")
async def get_all_ips(request: AllIPsInCountryRequest) -> str:
    logger.info("User sent post request for getting all addresses for a country.")
    res = server_controller.get_all_ips(request)
    if res.is_successful():
        logger.info("User received an answer for all addresses in a country.")
        return f"Here are all of the ip addresses in the country {request.country}: {res.get_data()}"
    logger.info("User received a failed answer for all addresses in a country.")
    return f"Something went wrong when looking for the ip's of {request.country}. The error is: {res.get_error_msg()}"


@server_router.get("/get_top_countries")
async def get_top_countries():
    logger.info("User sent get request for getting top 5 countries.")
    res = server_controller.get_top_countries()
    if res.is_successful():
        data = res.get_data()
        logger.info("User received an answer for top countries.")
        return f"Here are the top {len(data)} countries: {data}"
    logger.info("User received a failed answer for top countries.")
    return f"Something went wrong when looking for top 5 countries. The error is: {res.get_error_msg()}"

