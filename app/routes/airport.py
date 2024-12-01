from flask import Blueprint, render_template , session, flash, redirect, url_for , request, current_app
from app.clients.openaip_client import fetch_airport
from app.utils.auth import login_required
from app.libraries.preprocess import AirportProcessor
import boto3
import datetime

airport = Blueprint("airport", __name__ ,  template_folder="../templates/airport")

# Initialize the AirportProcessor class
processor = AirportProcessor()

@airport.route("/airport/<airport_id>")
def get_airport(airport_id):
    airport_data = fetch_airport(airport_id)

    if not airport_data:
        return render_template("error.html", message="Airport not found"), 404
    
    airport_data["is_favorite"] = processor.check_favorite_status(airport_id)
    return render_template("details.html", airport=airport_data)

@airport.route("/airport/<airport_id>/add_to_favorites", methods=["POST"])
@login_required
def add_to_favorites(airport_id):
   try:
        user_id = session["user_id"]
        airport_name = request.form.get("airport_name")
        airport_country = request.form.get("airport_country")

        # Get the DynamoDB table
        table = current_app.dynamodb.Table(current_app.config["DYNAMODB_FAVS_TABLE_NAME"])

        # Check if the airport is already added for this user
        response = table.get_item(Key={"user_id": user_id, "airport_id": airport_id})

        if "Item" in response:
            flash(f"'{airport_name}' is already in your favorites.", "info")
            return redirect(request.referrer or "/")

        # Add the airport to the user's favorites
        item = {
            "user_id": user_id,
            "airport_id": airport_id,
            "airport_name": airport_name,
            "airport_country": airport_country,
            "added_at": datetime.datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)
        flash(f"'{airport_name}' has been added to your favorites!", "success")
        return redirect(request.referrer or "/")
   except Exception as e:
        current_app.logger.error(f"Error adding to favorites: {e}")
        flash("An error occurred while adding the airport to favorites. Please try again.", "error")
        return redirect(request.referrer or "/")

@airport.route("/airport/<airport_id>/remove_from_favorites", methods=["POST"])
@login_required
def remove_from_favorites(airport_id):
    try:
        user_id = session["user_id"]

        # Get the DynamoDB table
        table = current_app.dynamodb.Table("skyport_favs")

        # Delete the item
        response = table.delete_item(
            Key={"user_id": user_id, "airport_id": airport_id}
        )

        flash("Airport removed from your favorites.", "success")
        return redirect(request.referrer or "/")

    except Exception as e:
        current_app.logger.error(f"Error removing from favorites: {e}")
        flash("An error occurred while removing the airport from favorites. Please try again.", "error")
        return redirect(request.referrer or "/")

@airport.route("/favorites")
@login_required
def favorites():
    try:
        user_id = session["user_id"]

        # Fetch user's favorites from DynamoDB
        table = current_app.dynamodb.Table("skyport_favs")
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(user_id)
        )

        favorites = response.get("Items", [])
        return render_template("favorites.html", favorites=favorites)

    except Exception as e:
        current_app.logger.error(f"Error fetching favorites: {e}")
        flash("An error occurred while fetching your favorites. Please try again.", "error")
        return redirect("/")


@airport.route("/airport/<airport_id>/add_memories", methods=["POST"])
@login_required
def add_memories(airport_id):
    # Logic to add memories for the airport
    user_id = session.get("user_id")  # Assume user_id is stored in the session
    # Save memory in the database (RDS or S3 for file uploads)

    flash(f"Memories added for airport {airport_id}.", "success")
    return redirect(url_for("airport.get_airport", airport_id=airport_id))
