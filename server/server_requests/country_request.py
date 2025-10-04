from pydantic import BaseModel


class CountryRequest(BaseModel):
    ip_address: str