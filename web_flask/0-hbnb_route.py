#!/usr/bin/python3

"""This module creates a single route to the root of the website"""

from web_flask import app


@app.route("/", strict_slashes=False)
def home():
    """Returns a simple string for the homepage"""
    return "Hello HBNB"
