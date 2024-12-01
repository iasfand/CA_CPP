import boto3
from flask import session, current_app

class AirportProcessor:
    def __init__(self):
        pass  # Avoid accessing current_app during initialization

    def get_dynamodb_table(self):
        """
        Fetch the DynamoDB table dynamically to ensure access during an active Flask context.
        """
        return current_app.dynamodb.Table("skyport_favs")

    def process_airports_data(self, airports):
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
                if len(coordinates) == 2
                else None
            )
            total_runways = len(airport.get("runways", []))

            # Check favorite status for this airport
            favorite_status = self.check_favorite_status(_id)

            processed_data.append(
                {
                    "id": _id,
                    "name": name,
                    "country": country,
                    "icaoCode": icaoCode,
                    "google_maps_link": google_maps_link,
                    "total_runways": total_runways,
                    "is_favorite": favorite_status,
                }
            )

        return processed_data

    def check_favorite_status(self, airport_id):
        """
        Check if a specific airport is a favorite for the logged-in user.

        Args:
            airport_id (str): The ID of the airport to check.

        Returns:
            bool: True if the airport is a favorite, False otherwise.
        """
        is_favorite = False

        if not session.get("logged_in"):
            return is_favorite

        user_id = session["user_id"]

        try:
            # Fetch DynamoDB table dynamically
            table = self.get_dynamodb_table()

            # Query DynamoDB to check if the record exists
            response = table.get_item(Key={"user_id": user_id, "airport_id": airport_id})

            if "Item" in response:
                is_favorite = True

        except Exception as e:
            current_app.logger.error(f"Error checking favorite status: {e}")

        return is_favorite
