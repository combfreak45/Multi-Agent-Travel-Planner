import http.client
import os
import json
import urllib.parse
# import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPID_APIKEY_FLIGHT")

def search_flights(source: str, destination: str, date: str, adults: int) -> dict:
    """
    Search for flights between two cities on a given date.
    
    Args:
        source (str): Source city code (e.g., "DEL" for Delhi). Convert city name to correct city code before calling.
        destination (str): Destination city code (e.g., "BOM" for Mumbai). Convert city name to correct city code before calling.
        date (str): Travel date in exactly YYYY-MM-DD format (e.g., "2023-11-30").
        adults (int): Number of adults for the trip, If user havent provide any input take 1.
    """
    conn = http.client.HTTPSConnection("google-flights2.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "e80de2b94emshc95078909e4f8d2p1fe304jsn8dbb354bed75",
        'x-rapidapi-host': "google-flights2.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    # note: have to figure out how to provide current date if user have not provide inputs for date.

    source = urllib.parse.quote(source)
    destination = urllib.parse.quote(destination)
    date = urllib.parse.quote(date)
    print(date)
    adults = urllib.parse.quote(str(adults))

    
    url = f"/api/v1/searchFlights?departure_id={source}&arrival_id={destination}&outbound_date={date}&travel_class=ECONOMY&adults={adults}&show_hidden=0&currency=INR&language_code=en-US&country_code=IN&search_type=best"

    try:
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"status": False, "message": f"Error occurred: {str(e)}", "data": []}