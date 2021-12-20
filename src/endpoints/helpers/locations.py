import urllib.parse
from typing import Dict
from typing import Optional
import httpx
from config import CONFIG


async def get_gps_coordinates(location: str) -> Optional[str]:
    """
    Get gps coordinates from a location
    :param location: `Street Name House Nr, City, Country`
    :return: `lat, lng`
    """
    if CONFIG.ext_api["test_mode"] == True:
        return test_response()

    enc_location = urllib.parse.quote(location)
    url_base = "http://api.positionstack"
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"http://api.positionstack.com/v1/forward?query={enc_location}&access_key={CONFIG.ext_api['positionstack_token']}")
    res_json = res.json()
    if not res_json["data"]:
        return None
    return f'{str(res_json["data"][0]["latitude"])},{str(res_json["data"][0]["longitude"])}'


async def get_route(origin: str, destination: str) -> Dict:
    """
    Get route from origin to destination
    :param origin: `lat, long`
    :param destination: `lat, long`
    :return: route
    """
    if CONFIG.ext_api["test_mode"] == True:
        return test_response()

    url = "https://api.openrouteservice.org/v2/directions/driving-hgv/json"
    headers = {
        "Authorization": f"{CONFIG.ext_api['ors_token']}",
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [[origin], [destination]]
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url=url,
            json=body,
            headers=headers)
    return res.json()


def test_response() -> str:
    return "40.755884,-73.978504"


if __name__ == "__main__":
    import asyncio
    asyncio.run(get_route("8.681495,49.41461", "8.686507,49.41943"))
