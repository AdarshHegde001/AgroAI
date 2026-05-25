import json
from pathlib import Path


DATA_PATH = Path(__file__).parent / "data" / "farmer_data.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_crops():
    return load_data().get("crops", [])


def get_pests():
    return load_data().get("pests", [])


def get_schemes():
    return load_data().get("schemes", [])


def get_market_prices():
    return load_data().get("market_prices", [])


def get_weather_samples():
    return load_data().get("weather_samples", [])


def get_sample_queries():
    return load_data().get("sample_queries", [])


def knowledge_base_summary():
    data = load_data()
    crop_names = ", ".join(crop["name"] for crop in data.get("crops", []))
    scheme_names = ", ".join(scheme["name"] for scheme in data.get("schemes", []))
    return (
        f"Available crops: {crop_names}. "
        f"Government schemes: {scheme_names}. "
        "Advice includes crop selection, fertilizer, pest control, irrigation, market prices, weather and sustainable farming."
    )
