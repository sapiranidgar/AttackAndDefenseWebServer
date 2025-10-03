from common_objects.responses import Response, DataResponse
from server.server_executor import Server
from server.server_requests.country_request import CountryRequest


class ServerController:
    __server = Server()
    def get_country(self, request: CountryRequest) -> Response[str]:
        ip_address = request.ip_address
        if self.__valid_ip_address(ip_address):
            country = self.__server.get_geolocation_by_address(ip_address)
            if country is None or country == "":
                return Response(error_msg="Failed to retrieve the ip's country", status_code=500)
            return DataResponse(country)
        else:
            return Response(error_msg="Invalid IP address.", status_code=400)

    @classmethod
    def __valid_ip_address(cls, ip_address: str) -> bool:
        ip_parts = ip_address.split('.')
        if len(ip_parts) != 4:
            return False
        for ip_part in ip_parts:
            if not ip_part.isdigit():
                return False
            i = int(ip_part)
            if i < 0 or i > 255:
                return False
        return True