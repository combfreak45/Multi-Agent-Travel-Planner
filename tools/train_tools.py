import http.client
import json
import urllib.parse
from config import rapidapi_key

def search_trains(start_station_code: str, end_station_code: str, date_of_journey_dd_mm_yyyy: str) -> dict:
    """
    Search for trains between two Indian railway stations on a given date.
    
    Args:
        start_station_code (str): Source station code (e.g., "NDLS" for New Delhi). Convert city name to correct station code before calling.
        end_station_code (str): Destination station code (e.g., "MMCT" for Mumbai Central). Convert city name to correct station code before calling.
        date_of_journey_dd_mm_yyyy (str): Travel date in exactly DD-MM-YYYY format (e.g., "30-11-2025").
    """
    conn = http.client.HTTPSConnection("irctc-api2.p.rapidapi.com")

    # Fallback to key temporarily if .env is missing so you aren't blocked!
    key = rapidapi_key if rapidapi_key else "e80de2b94emshc95078909e4f8d2p1fe304jsn8dbb354bed75"

    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "irctc-api2.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    start = urllib.parse.quote(start_station_code)
    end = urllib.parse.quote(end_station_code)
    date_formatted = urllib.parse.quote(date_of_journey_dd_mm_yyyy)

    url = f"/trainAvailability?source={start}&destination={end}&date={date_formatted}"

    try:
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"status": False, "message": f"Error occurred: {str(e)}", "data": []}
