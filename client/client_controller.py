from datetime import datetime
from typing import Optional

from client.client_executor import Client
from common_objects.responses import Response, DataResponse
from web_attacks.attack_type import AttackType

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

    def send_get_all_addresses_in_country_request(self, country: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Response[str]:
        try:
            server_answer = self.__client.send_get_all_addresses_in_country_request(country, start_date, end_date)
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

    def perform_syn_flood_attack(self, target_address: str, target_port: int, attack_type: AttackType,
                                 number_of_packets: int = NUMBER_OF_PACKETS) -> Response[bool]:
        try:
            if attack_type == AttackType.SYN_FLOOD_DIRECT:
                self.__client.perform_syn_flood_direct_attack(target_address, target_port, number_of_packets)
            elif attack_type == AttackType.SYN_FLOOD_SPOOFED:
                self.__client.perform_syn_flood_spoofed_attack(target_address, target_port, number_of_packets)
            else:
                return Response(error_msg="You chose unsupported syn-flood attack. Try again.", status_code=500)
            return DataResponse(True)
        except Exception as e:
            return Response(error_msg=f"Could not perform syn-flood spoofed attack. The error is: {e}",
                            status_code=500)

    def perform_url_brute_force_attack(self, target_address: str, target_port: int,
                                       number_of_packets: int = NUMBER_OF_PACKETS) -> Response[bool]:
        try:
            target_url = f"http://{target_address}:{target_port}"
            self.__client.perform_url_brute_force_attack(target_url, number_of_packets)
            return DataResponse(True)
        except Exception as e:
            return Response(error_msg=f"Could not perform url brute force attack. The error is: {e}", status_code=500)

    def perform_icmp_smurf_attack(self, target_address: str, number_of_packets: int):
        try:
            self.__client.perform_icmp_smurf_attack(target_address, number_of_packets)
            return DataResponse(True)
        except Exception as e:
            return Response(error_msg=f"Could not perform icmp smurf attack. The error is: {e}", status_code=500)

    def get_attack_details(self, attack_type: AttackType) -> Response[str]:
        try:
            details = self.__client.get_attack_details(attack_type)
            return DataResponse(details)
        except Exception as e:
            return Response(error_msg=f"Could not get details about the attack. The error is: {e}", status_code=500)
