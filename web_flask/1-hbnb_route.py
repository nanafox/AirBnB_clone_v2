#!/usr/bin/python3

"""This module contains routes for the AirBnB web project."""

from web_flask import app


@app.route("/", strict_slashes=False)
def home():
    """Returns a simple string for the homepage."""
    return "Hello HBNB"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Handles the /hbnb route."""
    return "HBNB"
