from flask import Blueprint, render_template , request, redirect, url_for, flash, current_app , session
from werkzeug.security import generate_password_hash , check_password_hash
from app.utils.auth import guest_required , login_required
import boto3
import uuid
import datetime

auth = Blueprint("auth", __name__ ,  template_folder="../templates/auth")

@auth.route("/login")
@guest_required
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    try:
        # Get form data
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate input
        if not email or not password:
            flash("Email and Password are required.", "error")
            return redirect(url_for("auth.login"))

        # Query DynamoDB for the user
        table = current_app.dynamodb.Table(current_app.config["DYNAMODB_TABLE_NAME"])
        response = table.query(
            IndexName="email-index",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
        )

        # Check if user exists
        if response["Count"] == 0:
            flash("User not found. Please register first.", "error")
            return redirect(url_for("auth.login"))

        # Get user data
        user = response["Items"][0]

        # Validate password
        if not check_password_hash(user["password"], password):
            flash("Incorrect password. Please try again.", "error")
            return redirect(url_for("auth.login"))

        # Store user information in session
        session["logged_in"] = True
        session["user_id"] = user["user_id"]
        session["user_name"] = user["name"]

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("main.index"))

    except Exception as e:
        current_app.logger.error(f"Error logging in: {e}")
        flash("An error occurred during login. Please try again.", "error")
        return redirect(url_for("auth.login"))

@auth.route("/register")
@guest_required
def register():
    return render_template("register.html")

@auth.route("/register", methods=["POST"])
def register_post():
    try:
        # Get request data
        staff_type = request.form.get("staff_type")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate input
        if not staff_type or not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        table = current_app.dynamodb.Table(current_app.config["DYNAMODB_TABLE_NAME"])
        # Check if email is already registered
        response = table.query(
            IndexName="email-index",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
        )

        if response["Count"] > 0:
            flash("Email is already registered. Please log in.", "error")
            return redirect(url_for("auth.login"))

        # Generate a unique user ID
        user_id = str(uuid.uuid4())

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Prepare user data
        user_data = {
            "user_id": user_id,
            "staff_type": staff_type,
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

        # Save to DynamoDB
        table.put_item(Item=user_data)

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    except Exception as e:
        current_app.logger.error(f"Error registering user: {e}")
        flash("An error occurred during registration. Please try again.", "error")
        return redirect(url_for("auth.register"))

@auth.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth.route("/profile")
def profile():
    # Check if user is logged in
    if not session.get("logged_in"):
        flash("You need to log in to view your profile.", "error")
        return redirect(url_for("auth.login"))
    
    try:
        # Fetch user_id from session
        user_id = session.get("user_id")

        # Query DynamoDB for the current user
        table = current_app.dynamodb.Table(current_app.config["DYNAMODB_TABLE_NAME"])
        response = table.get_item(Key={"user_id": user_id})
        # Check if user exists
        user = response.get("Item")
        if not user:
            flash("User not found.", "error")
            return redirect(url_for("main.index"))

        # Render profile page with user data
        return render_template("profile.html", user=user)

    except Exception as e:
        current_app.logger.error(f"Error fetching profile: {e}")
        flash("An error occurred while fetching your profile. Please try again.", "error")
        return redirect(url_for("main.index"))