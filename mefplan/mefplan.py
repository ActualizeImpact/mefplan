"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from . import styles

import reflex as rx


# Create the app.
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    title="MEF 90 Day Plan",
    description="A 90 Day Plan for the MEF team.",
)
