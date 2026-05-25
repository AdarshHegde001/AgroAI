from collections import Counter

import pandas as pd

from database import get_crops, get_market_prices, get_pests, get_schemes, get_weather_samples, load_data


def normalize(text):
    return text.lower().strip()


def find_crop_by_name(query):
    query = normalize(query)
    for crop in get_crops():
        if crop["name"].lower() in query:
            return crop
    return None


def recommend_crops(soil=None, season=None, water_need=None):
    crops = get_crops()
    results = []
    for crop in crops:
        score = 0
        reasons = []
        if soil and soil.lower() in [item.lower() for item in crop["soil"]]:
            score += 3
            reasons.append(f"suitable for {soil} soil")
        if season and season.lower() in [item.lower() for item in crop["season"]]:
            score += 2
            reasons.append(f"fits {season} season")
        if water_need and water_need.lower() == crop["water_need"].lower():
            score += 1
            reasons.append(f"{water_need} water requirement")
        if not reasons:
            reasons.append("general crop option from the knowledge base")
        results.append({"crop": crop, "score": score, "reasons": reasons})
    return sorted(results, key=lambda item: item["score"], reverse=True)


def fertilizer_recommendation(crop_name):
    for crop in get_crops():
        if crop["name"].lower() == crop_name.lower():
            fertilizers = ", ".join(crop["fertilizers"])
            return f"For {crop['name']}, commonly recommended inputs are {fertilizers}. Use soil test results before final dosage."
    return "Please mention a crop name. I can suggest common fertilizers using the knowledge base."


def irrigation_advice(crop_name=None, weather=None):
    crop = find_crop_by_name(crop_name or "") if crop_name else None
    if crop:
        base = f"{crop['name']} has {crop['water_need'].lower()} water need. "
    else:
        base = "For efficient irrigation, water according to crop stage and soil moisture. "

    if weather:
        rainfall = weather.get("rainfall", 0)
        temperature = weather.get("temperature", 30)
        if rainfall >= 8:
            return base + "Rainfall is expected, so delay irrigation and avoid waterlogging."
        if temperature >= 34:
            return base + "High temperature is expected, so irrigate early morning or evening and use mulching."
    return base + "Prefer drip or sprinkler systems, mulch the field, and avoid over-irrigation."


def pest_guidance(query):
    text = normalize(query)
    for pest in get_pests():
        searchable = " ".join([pest["crop"], pest["problem"], *pest["symptoms"]]).lower()
        if any(word in searchable for word in text.split()):
            return f"{pest['crop']} {pest['problem']}: {pest['management']}"
    return "Use regular field scouting, remove infected plant parts, prefer bio-control first, and consult a local agriculture officer before chemical spraying."


def government_scheme_response():
    lines = ["Important farmer support schemes:"]
    for scheme in get_schemes():
        lines.append(f"- {scheme['name']}: {scheme['benefit']} Action: {scheme['action']}")
    return "\n".join(lines)


def market_price_response(query):
    text = normalize(query)
    prices = get_market_prices()
    for item in prices:
        if item["crop"].lower() in text:
            return (
                f"Sample market guidance for {item['crop']}: around Rs. {item['price_per_quintal']} per quintal. "
                f"Trend: {item['trend']}. Please verify live mandi prices before selling."
            )
    return "Please mention a crop name. I can show sample market prices from the dataset."


def sustainable_tips():
    tips = load_data().get("sustainable_tips", [])
    return "Sustainable farming tips:\n" + "\n".join(f"- {tip}" for tip in tips)


def weather_advice():
    weather = get_weather_samples()
    avg_temp = round(sum(day["temperature"] for day in weather) / len(weather), 1)
    total_rain = sum(day["rainfall"] for day in weather)
    if total_rain > 30:
        advice = "Rainfall is moderate this week. Check drainage and reduce irrigation."
    elif avg_temp > 33:
        advice = "Hot conditions are expected. Use mulching and irrigate during cooler hours."
    else:
        advice = "Weather looks manageable. Continue crop-stage based irrigation and pest monitoring."
    return f"Weekly weather summary: average temperature {avg_temp} C, total rainfall {total_rain} mm. {advice}"


def detect_intent(query):
    text = normalize(query)
    keywords = {
        "crop": ["crop", "grow", "soil", "season", "black soil", "summer", "rabi", "kharif"],
        "fertilizer": ["fertilizer", "fertiliser", "urea", "dap", "npk", "nutrient"],
        "pest": ["pest", "disease", "leaf", "curl", "borer", "bollworm", "rust"],
        "irrigation": ["water", "irrigation", "drip", "sprinkler", "reduce water"],
        "scheme": ["scheme", "government", "subsidy", "pm-kisan", "insurance"],
        "market": ["market", "price", "mandi", "sell"],
        "weather": ["weather", "rain", "temperature", "humidity"],
        "sustainable": ["organic", "sustainable", "compost", "natural", "soil health"]
    }
    for intent, words in keywords.items():
        if any(word in text for word in words):
            return intent
    return "general"


def fallback_response(query):
    text = normalize(query)
    intent = detect_intent(text)

    if intent == "crop":
        soil = "black" if "black" in text else None
        season = next((s for s in ["summer", "kharif", "rabi", "winter", "monsoon"] if s in text), None)
        recs = recommend_crops(soil=soil, season=season)
        if recs:
            lines = ["Based on the knowledge base, suitable crop options are:"]
            for item in recs[:3]:
                lines.append(f"- {item['crop']['name']}: {', '.join(item['reasons'])}. Tip: {item['crop']['tips']}")
            return "\n".join(lines)
        return "Please share your soil type, season, and water availability so I can suggest crops."

    if intent == "fertilizer":
        crop = find_crop_by_name(text)
        return fertilizer_recommendation(crop["name"]) if crop else "Please mention the crop name for fertilizer guidance."

    if intent == "pest":
        return pest_guidance(text)

    if intent == "irrigation":
        crop = find_crop_by_name(text)
        return irrigation_advice(crop["name"] if crop else None)

    if intent == "scheme":
        return government_scheme_response()

    if intent == "market":
        return market_price_response(text)

    if intent == "weather":
        return weather_advice()

    if intent == "sustainable":
        return sustainable_tips()

    return (
        "I can help with crop selection, fertilizer, pest control, irrigation, weather, market prices, "
        "government schemes, and sustainable farming. Please ask a farming question in simple words."
    )


def crop_distribution_dataframe():
    rows = []
    for crop in get_crops():
        for soil in crop["soil"]:
            rows.append({"crop": crop["name"], "soil": soil, "water_need": crop["water_need"]})
    return pd.DataFrame(rows)


def crop_count_by_water_need():
    counts = Counter(crop["water_need"] for crop in get_crops())
    return pd.DataFrame({"water_need": list(counts.keys()), "count": list(counts.values())})


def market_dataframe():
    return pd.DataFrame(get_market_prices())


def weather_dataframe():
    return pd.DataFrame(get_weather_samples())
