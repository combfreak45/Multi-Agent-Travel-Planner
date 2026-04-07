import requests

def geocode(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    r = requests.get(url, params=params, headers={"User-Agent": "bus-route-agent"})
    r.raise_for_status()
    data = r.json()
    if not data:
        raise ValueError(f"No results for {query}")
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon

def route(lat1, lon1, lat2, lon2):
    url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    # 1. Geocode
    w_lat, w_lon = geocode("Whitefield Bangalore")
    m_lat, m_lon = geocode("Kempegowda Bus Station Bangalore")

    print("Whitefield:", w_lat, w_lon)
    print("Majestic:", m_lat, m_lon)

    # 2. Route
    data = route(w_lat, w_lon, m_lat, m_lon)

    route_info = data["routes"][0]
    print("Distance (m):", route_info["distance"])
    print("Duration (s):", route_info["duration"])
    print("Number of steps:", len(route_info["legs"][0]["steps"]))
