from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
from app.clients.openaip_client import fetch_airport
from app.utils.auth import login_required
from app.libraries.preprocess import AirportProcessor
from werkzeug.utils import secure_filename
import boto3
import datetime
import uuid

airport = Blueprint("airport", __name__, template_folder="../templates/airport")

# Initialize the AirportProcessor class
processor = AirportProcessor()


@airport.route("/airport/<airport_id>")
def get_airport(airport_id):
    try:
        current_app.logger.info(f"Fetching details for airport ID: {airport_id}")
        # Fetch airport data
        airport_data = fetch_airport(airport_id)
        if not airport_data:
            current_app.logger.warning(f"Airport not found: {airport_id}")
            return render_template("error.html", message="Airport not found"), 404

        # Check if airport is a favorite for the current user
        airport_data["is_favorite"] = processor.check_favorite_status(airport_id)

        # Determine the filter (All or Mine)
        filter_type = request.args.get("filter", "all")
        user_id = session.get("user_id") if filter_type == "mine" else None

        # Fetch memories based on the filter
        memories = fetch_memories(airport_id, user_id)

        current_app.logger.info(
            f"Loaded {len(memories)} memories for airport ID: {airport_id}, filter: {filter_type}"
        )

        return render_template(
            "details.html", airport=airport_data, memories=memories, filter_type=filter_type
        )

    except Exception as e:
        current_app.logger.error(f"Error fetching airport details for ID {airport_id}: {e}")
        return render_template("error.html", message="An error occurred"), 500


@airport.route("/airport/<airport_id>/add_to_favorites", methods=["POST"])
@login_required
def add_to_favorites(airport_id):
    try:
        user_id = session["user_id"]
        airport_name = request.form.get("airport_name")
        airport_country = request.form.get("airport_country")

        table = current_app.dynamodb.Table(current_app.config["DYNAMODB_FAVS_TABLE_NAME"])

        # Check if the airport is already added for this user
        response = table.get_item(Key={"user_id": user_id, "airport_id": airport_id})

        if "Item" in response:
            current_app.logger.info(
                f"User {user_id} attempted to re-add favorite airport {airport_id}."
            )
            flash(f"'{airport_name}' is already in your favorites.", "info")
            return redirect(request.referrer or "/")

        item = {
            "user_id": user_id,
            "airport_id": airport_id,
            "airport_name": airport_name,
            "airport_country": airport_country,
            "added_at": datetime.datetime.utcnow().isoformat(),
        }

        table.put_item(Item=item)
        current_app.logger.info(
            f"User {user_id} added airport {airport_id} ({airport_name}) to favorites."
        )
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

        table = current_app.dynamodb.Table("skyport_favs")
        table.delete_item(Key={"user_id": user_id, "airport_id": airport_id})

        current_app.logger.info(
            f"User {user_id} removed airport {airport_id} from favorites."
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

        table = current_app.dynamodb.Table("skyport_favs")
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(user_id)
        )

        favorites = response.get("Items", [])
        current_app.logger.info(f"User {user_id} fetched {len(favorites)} favorite airports.")
        return render_template("favorites.html", favorites=favorites)
    except Exception as e:
        current_app.logger.error(f"Error fetching favorites: {e}")
        flash("An error occurred while fetching your favorites. Please try again.", "error")
        return redirect("/")


@airport.route("/airport/<airport_id>/add_memories", methods=["POST"])
@login_required
def add_memories(airport_id):
    try:
        user_id = session["user_id"]
        file = request.files["photo"]

        if not file:
            current_app.logger.warning(f"No file selected for memory upload by user ID: {user_id}")
            flash("No file selected.", "error")
            return redirect(url_for("airport.get_airport", airport_id=airport_id))

        # Secure and unique file naming
        filename = secure_filename(file.filename)
        unique_filename = f"{user_id}/{airport_id}/{uuid.uuid4().hex}_{filename}"

        # Upload to S3
        s3_client = current_app.s3_client
        s3_client.upload_fileobj(
            file,
            current_app.config["S3_BUCKET_NAME"],
            unique_filename,
            ExtraArgs={"ContentType": file.content_type},
        )
        current_app.logger.info(
            f"Uploaded memory to S3 for user {user_id}, airport {airport_id}, file: {unique_filename}"
        )

        # Save metadata to DynamoDB
        dynamodb = current_app.dynamodb.Table(current_app.config["DYNAMODB_MEMO_TABLE_NAME"])
        dynamodb.put_item(
            Item={
                "airport_id": airport_id,
                "user_id_photo_id": f"{user_id}#{uuid.uuid4().hex}",
                "photo_url": f"https://{current_app.config['S3_BUCKET_NAME']}.s3.amazonaws.com/{unique_filename}",
                "filename": unique_filename,
                "uploaded_at": datetime.datetime.utcnow().isoformat(),
            }
        )
        current_app.logger.info(
            f"Saved memory metadata to DynamoDB for user {user_id}, airport {airport_id}"
        )

        flash("Memory uploaded successfully!", "success")
        return redirect(url_for("airport.get_airport", airport_id=airport_id))
    except Exception as e:
        current_app.logger.error(f"Error uploading memory for user ID {user_id}, airport ID {airport_id}: {e}")
        flash("An error occurred while uploading the memory. Please try again.", "error")
        return redirect(url_for("airport.get_airport", airport_id=airport_id))


def fetch_memories(airport_id, user_id=None):
    try:
        table = current_app.dynamodb.Table(current_app.config["DYNAMODB_MEMO_TABLE_NAME"])
        s3_client = current_app.s3_client

        key_condition = boto3.dynamodb.conditions.Key("airport_id").eq(airport_id)
        response = table.query(KeyConditionExpression=key_condition)
        items = response.get("Items", [])

        if user_id:
            items = [item for item in items if item["user_id_photo_id"].startswith(user_id)]

        for item in items:
            item["photo_url"] = s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": current_app.config["S3_BUCKET_NAME"],
                    "Key": item["filename"],
                },
                ExpiresIn=3600,
            )

        current_app.logger.info(
            f"Fetched {len(items)} memories for airport ID {airport_id}, user ID: {user_id}"
        )
        return items
    except Exception as e:
        current_app.logger.error(f"Error fetching memories for airport ID {airport_id}: {e}")
        return []
