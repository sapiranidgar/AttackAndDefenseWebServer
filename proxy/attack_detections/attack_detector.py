from abc import ABC, abstractmethod


class AttackDetector(ABC):

    @abstractmethod
    def analyze_single_packet(self, pkt):
        pass

    @abstractmethod
    def get_ips_to_block(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def reset_detector(self):
        pass