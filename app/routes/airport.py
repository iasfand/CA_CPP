from flask import Blueprint, render_template , session, flash, redirect, url_for
from app.clients.openaip_client import fetch_airport
from app.utils.auth import login_required

airport = Blueprint("airport", __name__ ,  template_folder="../templates/airport")

@airport.route("/airport/<airport_id>")
def get_airport(airport_id):
    airport_data = fetch_airport(airport_id)

    if not airport_data:
        return render_template("error.html", message="Airport not found"), 404

    return render_template("details.html", airport=airport_data)

@airport.route("/airport/<airport_id>/add_to_favorites", methods=["POST"])
@login_required
def add_to_favorites(airport_id):
    # Logic to add airport to user's favorites
    user_id = session.get("user_id")  # Assume user_id is stored in the session
    # Save favorite in the database (RDS or any storage)

    flash(f"Airport {airport_id} added to your favorites.", "success")
    return redirect(url_for("airport.get_airport", airport_id=airport_id))

@airport.route("/airport/<airport_id>/add_memories", methods=["POST"])
@login_required
def add_memories(airport_id):
    # Logic to add memories for the airport
    user_id = session.get("user_id")  # Assume user_id is stored in the session
    # Save memory in the database (RDS or S3 for file uploads)

    flash(f"Memories added for airport {airport_id}.", "success")
    return redirect(url_for("airport.get_airport", airport_id=airport_id))
