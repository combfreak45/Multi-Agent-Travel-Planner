import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def search_flights(source: str, destination: str, date: str, travel_class: str = "ECONOMY", adults: int = 1) -> dict:
    """
    Search for flights using Google Flights.
    source and destination are IATA airport codes e.g. DEL, BOM, BLR, LAX, JFK.
    date must be in YYYY-MM-DD format.
    travel_class options: ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
    """
    url = "https://google-flights2.p.rapidapi.com/api/v1/searchFlights"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "google-flights2.p.rapidapi.com"
    }

    params = {
        "departure_id": source,
        "arrival_id": destination,
        "outbound_date": date,
        "travel_class": travel_class,
        "adults": str(adults),
        "show_hidden": "1",
        "currency": "INR",
        "language_code": "en-US",
        "country_code": "IN",
        "search_type": "best"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "message" in data:
            return {"error": data["message"]}

        flights = []
        itineraries = data.get("data", {}).get("itineraries", [])

        if not itineraries:
            return {"message": "No flights found", "raw": data}

        for item in itineraries[:5]:
            try:
                leg = item["legs"][0]
                flights.append({
                    "airline": leg["carriers"]["marketing"][0]["name"],
                    "flight_number": leg["carriers"]["marketing"][0].get("flightNumber", "N/A"),
                    "departure": leg["departure"],
                    "arrival": leg["arrival"],
                    "duration_mins": leg["durationInMinutes"],
                    "stops": leg["stopCount"],
                    "price": item["price"]["formatted"],
                })
            except (KeyError, IndexError):
                continue

        return {"flights": flights}

    except Exception as e:
        return {"error": str(e)}