from client.client_executor import Client
from common_objects.responses import Response, DataResponse
from web_attacks.attack_type import SynFloodAttackType


NUMBER_OF_PACKETS = 10
MIN_NUMBER_OF_PACKETS_FOR_ATTACK = 10

class ClientController:
    def __init__(self):
        self.__client = Client()

    def send_country_request(self, ip_address: str) -> Response[str]:
        try:
            server_answer = self.__client.send_country_request(ip_address)
            return DataResponse(server_answer)
        except Exception as e:
            return Response(error_msg=f"Could not receive the country for ip {ip_address}. The error is: {e}",
                            status_code=500)

    def send_get_all_addresses_in_country_request(self, country: str) -> Response[str]:
        try:
            server_answer = self.__client.send_get_all_addresses_in_country_request(country)
            return DataResponse(server_answer)
        except Exception as e:
            return Response(error_msg=f"Could not receive the addresses of country {country}. The error is: {e}",
                            status_code=500)

    def send_get_top_countries_request(self) -> Response[str]:
        try:
            server_answer = self.__client.send_get_top_countries_request()
            return DataResponse(server_answer)
        except Exception as e:
            return Response(error_msg=f"Could not receive top countries. The error is: {e}",
                            status_code=500)

    def perform_syn_flood_attack(self, target_address: str, target_port: int, attack_type: SynFloodAttackType,
                                 number_of_packets: int = NUMBER_OF_PACKETS) -> Response[bool]:
        if not self.__valid_number_of_packets(number_of_packets):
            return Response(error_msg=f"Number of packets to perform the attack is too small. Try again with at least {MIN_NUMBER_OF_PACKETS_FOR_ATTACK} packets.")
        if attack_type == SynFloodAttackType.DIRECT:
            try:
                self.__client.perform_syn_flood_direct_attack(target_address, target_port, number_of_packets)
                return DataResponse(True)
            except Exception as e:
                return Response(error_msg=f"Could not perform syn-flood direct attack. The error is: {e}",
                                status_code=500)
        elif attack_type == SynFloodAttackType.SPOOFED:
            try:
                self.__client.perform_syn_flood_spoofed_attack(target_address, target_port, number_of_packets)
                return DataResponse(True)
            except Exception as e:
                return Response(error_msg=f"Could not perform syn-flood spoofed attack. The error is: {e}",
                                status_code=500)
        else:
            return Response(error_msg="You chose unsupported syn-flood attack. Try again.", status_code=500)

    def perform_url_brute_force_attack(self, target_address: str, number_of_packets: int = NUMBER_OF_PACKETS) -> Response[bool]:
        if not self.__valid_number_of_packets(number_of_packets):
            return Response(
                error_msg=f"Number of packets to perform the attack is too small. Try again with at least {MIN_NUMBER_OF_PACKETS_FOR_ATTACK} packets.")

        try:
            target_url = "http://" + target_address
            self.__client.perform_url_brute_force_attack(target_url, number_of_packets)
            return DataResponse(True)
        except Exception as e:
            return Response(error_msg=f"Could not perform url brute force attack. The error is: {e}", status_code=500)

    def perform_third_attack(self, target_address: str, target_port: int):
        pass

    def __valid_number_of_packets(self, number_of_packets: int) -> bool:
        if number_of_packets < MIN_NUMBER_OF_PACKETS_FOR_ATTACK:
            return False
        return True
