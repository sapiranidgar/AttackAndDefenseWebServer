from datetime import datetime
from typing import Optional

from server.server_requests.server_request import ServerRequest


class AllIPsInCountryRequest(ServerRequest):
    country: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
