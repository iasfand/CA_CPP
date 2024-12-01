import requests
from flask import current_app

def fetch_openaip_data(endpoint, page=1, limit=100, country=None):
    """
    Fetch data from OpenAIP API.

    Args:
        endpoint (str): API endpoint to fetch data from.
        page (int): Page number for pagination.
        limit (int): Number of results per page.
        country (str): Optional country code to filter results.

    Returns:
        dict: Parsed JSON response from the API or None in case of an error.
    """
    base_url = f"{current_app.config['OPENAIP_API_URL']}/{endpoint}"
    headers = {
        "accept": "application/json",
        "x-openaip-api-key": current_app.config['OPENAIP_API_KEY']
    }
    params = {
        "page": page,
        "limit": limit
    }

    # Add country filter if provided
    if country:
        params["country"] = country

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        current_app.logger.error(f"OpenAIP API error: {e}")
        return None


def fetch_airport(airport_id):
    """
    Fetch a single airport by its ID from OpenAIP API.

    Args:
        airport_id (str): The unique ID of the airport.

    Returns:
        dict: Parsed JSON response containing the airport details or None in case of an error.
    """
    base_url = f"{current_app.config['OPENAIP_API_URL']}/airports/{airport_id}?apiKey={current_app.config['OPENAIP_API_KEY']}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        current_app.logger.error(f"Error fetching airport ID {airport_id}: {e}")
        return None
