from fastapi import FastAPI

from server.server_requests.country_request import CountryRequest

app = FastAPI()


@app.post("/get_country")
async def get_ip_country(request: CountryRequest):
    return {"message": request.ip_address}