#!/usr/bin/python3

"""This module creates a single route to the root of the website"""

from web_flask import app


@app.route("/", strict_slashes=False)
def home():
    """Returns a simple string for the homepage"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
