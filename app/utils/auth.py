from functools import wraps
from flask import session, redirect, url_for, flash

def guest_required(f):
    """
    Decorator to ensure the user is not logged in before accessing a route.

    Args:
        f (function): The route function being decorated.

    Returns:
        function: A wrapped function that checks user authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in"):
            flash("You are already logged in.", "warning")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """
    Decorator to ensure the user is logged in before accessing a route.

    Args:
        f (function): The route function being decorated.

    Returns:
        function: A wrapped function that checks user authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("You need to log in to perform this action.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
