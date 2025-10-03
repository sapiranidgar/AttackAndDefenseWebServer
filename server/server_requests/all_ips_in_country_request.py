from pydantic import BaseModel


class AllIPsInCountryRequest(BaseModel):
    country: str