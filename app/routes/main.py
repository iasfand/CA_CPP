from flask import Blueprint, render_template, request
from app.clients.openaip_client import fetch_openaip_data
from app.libraries.preprocess import process_airports_data
import json

main = Blueprint("main", __name__)

@main.route("/")
def index():
    # Pagination parameters
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=100, type=int)
    country = request.args.get("country", default=None, type=str)


    # Load countries from static JSON file
    with open("app/data/countries.json") as f:
        countries = json.load(f)
    # Fetch airports with the specified parameters
    data = fetch_openaip_data("airports", page=page, limit=limit , country=country)
    airports = data.get("items", [])
    total_items = data.get("totalCount", 0)
    total_pages = data.get("totalPages" , (total_items + limit - 1) // limit)  # Calculate total pages
    from_page = (page - 1) * limit + 1
    to_page = min(page * limit, total_items)
    processed_data = process_airports_data(airports)
    return render_template(
        "index.html",
        title="Airports",
        info={
            "items": processed_data,
            "current_page": page,
            "from_page": from_page,
            "to_page": to_page,
            "total_items": total_items,
            "total_pages": total_pages,
            "countries": countries,
            "selected_country": country,
        },
    )
