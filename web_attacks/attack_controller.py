import threading

from web_attacks.attack_parameters import AttackParameters
from web_attacks.attack_type import AttackType
from web_attacks.attacks.icmp_smurf_attack import ICMPSmurfAttack
from web_attacks.attacks.syn_flood_attack import SynFloodDirectAttack, SynFloodSpoofedAttack
from web_attacks.attacks.url_brute_force_attack import UrlBruteForceAttack


class AttackController:
    __attacks = {
        AttackType.URL_BRUTE_FORCE: UrlBruteForceAttack(),
        AttackType.ICMP_SMURF: ICMPSmurfAttack(),
        AttackType.SYN_FLOOD_DIRECT: SynFloodDirectAttack(),
        AttackType.SYN_FLOOD_SPOOFED: SynFloodSpoofedAttack()
    }
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        raise RuntimeError("This is a Singleton. Invoke get_instance() instead.")

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)

        return cls.__instance

    def perform_attack(self, attack_parameters: AttackParameters, attack_type: AttackType):
        if attack_type in self.__attacks:
            self.__attacks[attack_type].perform_attack(attack_parameters)
        else:
            raise Exception(f"Invalid attack type: {attack_type}")

    def get_attack_details(self, attack_type: AttackType):
        if attack_type in self.__attacks:
            return self.__attacks[attack_type].get_attack_details()
        else:
            raise Exception(f"Invalid attack type: {attack_type}")
