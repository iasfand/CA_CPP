import requests
from flask import current_app

def fetch_openaip_data(endpoint, page=1, limit=100):
    print("fetch_openaip_data" , endpoint , page , limit)
    """
    Fetch  data from OpenAIP API.

    Args:
        endpoint (str): API endpoint to fetch data from.
        page (int): Page number for pagination.
        limit (int): Number of results per page.

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

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        current_app.logger.error(f"OpenAIP API error: {e}")
        return None
