from enum import Enum


class AttackType(Enum):
    SYN_FLOOD_DIRECT = 1
    SYN_FLOOD_SPOOFED = 2
    URL_BRUTE_FORCE = 3
    ICMP_SMURF = 4
