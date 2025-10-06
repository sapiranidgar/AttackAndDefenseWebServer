import random


def generate_random_ip() -> str:
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip


def generate_random_big_int() -> int:
    x = random.randint(1000, 9000)
    return x
