import reflex as rx

dashboard_style = {
    "card": {
        "border_radius": "10px",
        "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "transition": "all 0.3s ease-in-out",
        "_hover": {
            "box_shadow": "0 6px 8px rgba(0, 0, 0, 0.15)",
            "transform": "translateY(-2px)",
        },
    },
    "heading": {
        "color": "blue.600",
        "font_weight": "bold",
    },
    "chart": {
        "font_family": "Arial, sans-serif",
    },
}


def apply_dashboard_style(component):
    return rx.style(component, **dashboard_style)
