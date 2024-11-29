def process_airports_data(airports):
    """
    Process an array of airport dictionaries and extract desired information.
    
    Args:
        airports (list): List of dictionaries containing airport data.
        
    Returns:
        list: Processed airport information.
    """
    processed_data = []
    for airport in airports:
        _id = airport.get("_id")
        name = airport.get("name")
        country = airport.get("country")
        icaoCode = airport.get("icaoCode") or "-"
        coordinates = airport.get("geometry", {}).get("coordinates", [])
        google_maps_link = (
            f"https://www.google.com/maps/search/?api=1&query={coordinates[1]},{coordinates[0]}"
            if len(coordinates) == 2 else None
        )
        total_runways = len(airport.get("runways", []))
        
        processed_data.append({
            "id": _id,
            "name": name,
            "country": country,
            "icaoCode": icaoCode,
            "google_maps_link": google_maps_link,
            "total_runways": total_runways
        })
    
    return processed_data
