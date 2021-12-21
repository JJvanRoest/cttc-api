import urllib.parse
from typing import Dict
from typing import Optional, List, Tuple
import httpx
from config import CONFIG
import json
from ...database.locations import Locations
from ...database.database import database as db


async def get_gps_coordinates(location: str) -> Optional[str]:
    """
    Get gps coordinates from a location
    :param location: `Street Name House Nr, City, Country`
    :return: `lat, lng`
    """
    if CONFIG.ext_api["test_mode"] == True:
        return test_response()
    with db.atomic():
        db_location: Optional[Locations] = Locations.get_or_none(
            Locations.location == location)
    if db_location is None:
        res = await get_positionstack_coordinates(location)
        res_json = res.json()
        if res_json["data"] == [[], []]:
            return None
        Locations.create(
            location=location,
            location_data=res_json
        )
    else:
        res_json = db_location.location_data

    return f'{str(res_json["data"][0]["latitude"])},{str(res_json["data"][0]["longitude"])}'


async def get_route(coordinates: List[str]) -> Dict:
    """
    Get route from origin to destination
    :param coordinates: [`lat,long`, `lat,long`]
    :return: route
    """
    if CONFIG.ext_api["test_mode"] == True:
        return test_response()

    url = "https://api.openrouteservice.org/v2/directions/driving-car/json"
    headers = {
        "Authorization": f"{CONFIG.ext_api['ors_token']}",
        "Content-Type": "application/json"
    }
    attributes = ["avgspeed"]
    preference = "recommended"
    maximum_speed = 90
    coordinate_body: List = []
    for coordinate in coordinates:
        tuples = coordinate.split(",")
        coordinate_body.append([float(tuples[1]), float(tuples[0])])
    body = {
        "coordinates": coordinate_body,
        "attributes": attributes,
        "preference": preference,
        "maximum_speed": maximum_speed,


    }
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url=url,
            json=body,
            headers=headers)
    if res.status_code != 200:
        raise ValueError(f"Error getting route: {res.json()}")
    return res.json()


def test_response() -> str:
    return "40.755884,-73.978504"


def test_route() -> Dict:
    return httpx.Response(status_code=200, json="""
    {"routes":[{"summary":{"distance":3501.9,"duration":666.8},"segments":[{"distance":890.9,"duration":189.6,"steps":[{"distance":1.9,"duration":0.5,"type":11,"instruction":"Head west on Gerhart-Hauptmann-Straße","name":"Gerhart-Hauptmann-Straße","way_points":[0,1]},{"distance":314,"duration":75.4,"type":3,"instruction":"Turn sharp right onto Wielandtstraße","name":"Wielandtstraße","way_points":[1,11]},{"distance":251.7,"duration":36.2,"type":1,"instruction":"Turn right onto Mönchhofstraße","name":"Mönchhofstraße","way_points":[11,22]},{"distance":211.8,"duration":50.8,"type":0,"instruction":"Turn left onto Keplerstraße","name":"Keplerstraße","way_points":[22,28]},{"distance":109.5,"duration":26.3,"type":1,"instruction":"Turn right onto Moltkestraße","name":"Moltkestraße","way_points":[28,31]},{"distance":2,"duration":0.5,"type":0,"instruction":"Turn left onto Werderplatz","name":"Werderplatz","way_points":[31,32]},{"distance":0,"duration":0,"type":10,"instruction":"Arrive at Werderplatz, on the right","name":"-","way_points":[32,32]}],"avgspeed":16.92},{"distance":847.7,"duration":170.2,"steps":[{"distance":2,"duration":0.5,"type":11,"instruction":"Head south on Werderplatz","name":"Werderplatz","way_points":[32,33]},{"distance":43.3,"duration":10.4,"type":0,"instruction":"Turn left onto Moltkestraße","name":"Moltkestraße","way_points":[33,35]},{"distance":237.7,"duration":57,"type":1,"instruction":"Turn right onto Werderstraße","name":"Werderstraße","way_points":[35,43]},{"distance":346.6,"duration":49.9,"type":1,"instruction":"Turn right onto Mönchhofstraße","name":"Mönchhofstraße","way_points":[43,55]},{"distance":218.2,"duration":52.4,"type":0,"instruction":"Turn left onto Maulbeerweg","name":"Maulbeerweg","way_points":[55,63]},{"distance":0,"duration":0,"type":10,"instruction":"Arrive at Maulbeerweg, on the left","name":"-","way_points":[63,63]}],"avgspeed":17.93},{"distance":1763.3,"duration":307,"steps":[{"distance":98.2,"duration":23.6,"type":11,"instruction":"Head south on Maulbeerweg","name":"Maulbeerweg","way_points":[63,65]},{"distance":63.2,"duration":15.2,"type":1,"instruction":"Turn right onto Gerhart-Hauptmann-Straße","name":"Gerhart-Hauptmann-Straße","way_points":[65,68]},{"distance":314,"duration":75.4,"type":3,"instruction":"Turn sharp right onto Wielandtstraße","name":"Wielandtstraße","way_points":[68,78]},{"distance":737.6,"duration":106.2,"type":1,"instruction":"Turn right onto Mönchhofstraße","name":"Mönchhofstraße","way_points":[78,106]},{"distance":264.3,"duration":41.4,"type":0,"instruction":"Turn left onto Handschuhsheimer Landstraße, B 3","name":"Handschuhsheimer Landstraße, B 3","way_points":[106,124]},{"distance":155.3,"duration":14,"type":5,"instruction":"Turn slight right onto Handschuhsheimer Landstraße, B 3","name":"Handschuhsheimer Landstraße, B 3","way_points":[124,128]},{"distance":130.8,"duration":31.4,"type":0,"instruction":"Turn left onto Roonstraße","name":"Roonstraße","way_points":[128,131]},{"distance":0,"duration":0,"type":10,"instruction":"Arrive at Roonstraße, straight ahead","name":"-","way_points":[131,131]}],"avgspeed":20.68}],"bbox":[8.681423,49.414554,8.69198,49.420514],"geometry":"ghrlHkr~s@?DICqELI?IAsCi@ICKAuA_@i@GSA?_@?M?eA?S?W?S@wB@k@?U@{H?MI@I@u@FkBP{Db@I@?M[mGAMC?B?KiB?KFAtAKjBSFADApBWrAGHC?PCbC?|@?jC?t@@N?LAzH?TAj@AvB?RL@zC@H?F@dCNF@H@r@HdD\\H@AHInC@RICqELI?IAsCi@ICKAuA_@i@GSA?_@?M?eA?S?W?S@wB@k@?U@{H?MAO?u@?kC?}@BcC?Q?OAmCCkBEoFAu@?M?Qt@oEHu@Ck@?CSFA@OHKJgAlA_AfAUREDC?Q?OBE@qBn@A@SHOJELCDgAb@q@\\mAt@y@f@?BVlELpC","way_points":[0,32,63,131]}],"bbox":[8.681423,49.414554,8.69198,49.420514],"metadata":{"attribution":"openrouteservice.org | OpenStreetMap contributors","service":"routing","timestamp":1640073992050,"query":{"coordinates":[[8.681495,49.41461],[8.686507,49.41943],[8.682507,49.41543],[8.687872,49.420318]],"profile":"driving-hgv","preference":"fastest","format":"json","attributes":["avgspeed"],"maximum_speed":90},"engine":{"version":"6.6.3","build_date":"2021-12-16T11:22:41Z","graph_date":"2021-12-12T08:51:37Z"},"system_message":"Preference 'fastest' has been deprecated, using 'recommended'."}}
    """)


async def get_positionstack_coordinates(location: str) -> httpx.Response:
    enc_location = urllib.parse.quote(location)
    url_base = "http://api.positionstack.com/v1"
    request = f"{url_base}/forward?query={enc_location}&access_key={CONFIG.ext_api['positionstack_token']}"
    timeout = httpx.Timeout(10.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        res = await client.get(request)
    return res
