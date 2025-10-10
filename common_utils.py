def is_valid_ip_address(ip_address: str) -> bool:
    ip_parts = ip_address.split('.')
    if len(ip_parts) != 4:
        return False
    for ip_part in ip_parts:
        if not ip_part.isdigit():
            return False
        i = int(ip_part)
        if i < 0 or i > 255:
            return False
    return True