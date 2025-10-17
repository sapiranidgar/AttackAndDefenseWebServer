import threading
import time

from scapy.config import conf
from scapy.sendrecv import sniff

from proxy.attack_detections.syn_flood_attack_detector import SynFloodAttackDetector
from proxy.proxy_controller import ProxyController

SLEEP_TIME_BETWEEN_REQUESTS = 5


class AttackMonitor:
    def __init__(self):
        self.__attacks_detectors = [SynFloodAttackDetector()]
        self.__proxy_controller = ProxyController()

    def detect_attacks(self):
        while True:
            time.sleep(SLEEP_TIME_BETWEEN_REQUESTS)
            for attack_detector in self.__attacks_detectors:
                self.__block_attackers(attack_detector.get_ips_to_block())

            self.__reset_attacks_detectors()


    def __block_attackers(self, ips_and_reasons: list[tuple[str, str]]):
        for ip, reason in ips_and_reasons:
            print("blocked IP: {}, REASON: {}".format(ip, reason))
            self.__proxy_controller.block_ip(ip, reason)

    def analyze_packet(self, packet):
        for attack_detector in self.__attacks_detectors:
            attack_detector.analyze_single_packet(packet)


    def start_attack_monitor(self):
        """Start Scapy sniffer and detection thread."""
        print("[MONITOR] Attack detection started...")
        threading.Thread(target=self.detect_attacks, daemon=True).start()

        try:
            sniff(
                iface=["\\Device\\NPF_Loopback", conf.iface],
                prn=self.analyze_packet,
                store=False
            )
        except Exception as e:
            print(f"[MONITOR] Error: {e}")

    def __reset_attacks_detectors(self):
        for attack_detector in self.__attacks_detectors:
            attack_detector.reset_detector()
