from scapy.all import *
from collections import Counter
import threading
import time

from scapy.layers.inet import IP, TCP

from proxy_controller import ProxyController

SLEEP_TIME_BETWEEN_REQUESTS = 5
SYN_COUNT_FOR_SYN_FLOOD_DETECTION = 10

syn_count = Counter()
ack_count = Counter()


def analyze_syn_ack(pkt):
    """Analyze TCP packets for SYN flood patterns."""

    if IP in pkt and TCP in pkt:
        src = pkt[IP].src

        if pkt[TCP].flags.S:
            syn_count[src] += 1
        elif pkt[TCP].flags.A:
            ack_count[src] += 1


def detect_attacks():
    """Periodically check packet counts for DoS patterns."""
    controller = ProxyController.get_instance()

    while True:
        time.sleep(SLEEP_TIME_BETWEEN_REQUESTS)
        if not syn_count:
            continue

        for src, syns in syn_count.items():
            acks = ack_count.get(src, 0)
            if syns > 3 * acks and syns > SYN_COUNT_FOR_SYN_FLOOD_DETECTION:
                controller.block_ip(src, reason="SYN Flood detected")
        syn_count.clear()
        ack_count.clear()


def start_attack_monitor():
    """Start Scapy sniffer and detection thread."""
    print("[MONITOR] Attack detection started...")
    threading.Thread(target=detect_attacks, daemon=True).start()

    try:
        sniff(
            iface=["\\Device\\NPF_Loopback", conf.iface],
            prn=analyze_syn_ack,
            store=False
        )
    except Exception as e:
        print(f"[MONITOR] Error: {e}")
