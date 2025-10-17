import logging
import threading
import time

from scapy.config import conf
from scapy.sendrecv import sniff

from proxy.attack_detections.icmp_smurf_attack_detector import ICMPSmurfAttackDetector
from proxy.attack_detections.regular_dos_attack_detector import RegularDosAttackDetector
from proxy.attack_detections.syn_flood_attack_detector import SynFloodAttackDetector
from proxy.attack_detections.url_brute_force_attack_detector import UrlBruteForceAttackDetector
from proxy.proxy_controller import ProxyController

logger = logging.getLogger(__name__)

SLEEP_TIME_BETWEEN_REQUESTS = 5


class AttackMonitor:
    """
    This class detects possible attacks and the attackers who caused them.
    The attacks that can be detected are:
    1. Syn-Flood Attack
    2. Regular DOS Attack
    3. URL-Brute Force Attack
    """

    def __init__(self):
        self.__attacks_detectors = [SynFloodAttackDetector(), UrlBruteForceAttackDetector(),
                                    RegularDosAttackDetector(), ICMPSmurfAttackDetector()]
        self.__proxy_controller = ProxyController()

    def detect_attacks(self):
        while True:
            logger.info("Attack Monitor: looking for possible attacks.")
            time.sleep(SLEEP_TIME_BETWEEN_REQUESTS)
            for attack_detector in self.__attacks_detectors:
                self.__block_attackers(attack_detector.get_ips_to_block())

            self.__reset_attacks_detectors()

    def __block_attackers(self, ips_and_reasons: list[tuple[str, str]]):
        for ip, reason in ips_and_reasons:
            self.__proxy_controller.block_ip(ip, reason)

    def analyze_packet(self, packet):
        for attack_detector in self.__attacks_detectors:
            attack_detector.analyze_single_packet(packet)

    def start_attack_monitor(self):
        """Start Scapy sniffer and detection thread."""
        logger.info("Attack Monitor: START.")
        threading.Thread(target=self.detect_attacks, daemon=True).start()

        try:
            sniff(
                iface=["\\Device\\NPF_Loopback", conf.iface],
                prn=self.analyze_packet,
                store=False
            )
        except Exception as e:
            logger.info(f"Attack Monitor: Error occurred - {e}.")

    def __reset_attacks_detectors(self):
        for attack_detector in self.__attacks_detectors:
            attack_detector.reset_detector()
