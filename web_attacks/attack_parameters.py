from typing import Optional

from pydantic import BaseModel


class AttackParameters(BaseModel):
    target_ip: str
    target_port: Optional[int] = None
    num_of_requests: int
