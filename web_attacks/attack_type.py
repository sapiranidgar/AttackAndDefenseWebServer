from enum import Enum


class AttackType(Enum):
    SYN_FLOOD = 1
    URL_BRUTE_FORCE = 2
    ICMP_SMURF = 3

class SynFloodAttackType(Enum):
    DIRECT = 1
    SPOOFED = 2