import matplotlib.pyplot as plt
import streamlit as st

from chatbot import AgroAidChatbot
from database import get_crops, get_sample_queries, load_data
from utils import (
    crop_count_by_water_need,
    crop_distribution_dataframe,
    fertilizer_recommendation,
    government_scheme_response,
    irrigation_advice,
    market_dataframe,
    pest_guidance,
    recommend_crops,
    sustainable_tips,
    weather_advice,
    weather_dataframe,
)


st.set_page_config(
    page_title="AgroAid AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


CSS = """
<style>
    .main { background: #f6f8f4; }
    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f5132, #2f8f46);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; font-size: 2.2rem; }
    .hero p { margin: .4rem 0 0; font-size: 1.02rem; opacity: .96; }
    .metric-card {
        padding: 1rem;
        border-radius: 14px;
        background: white;
        color: #203125;
        border: 1px solid #dfe8dc;
        box-shadow: 0 2px 12px rgba(22, 74, 39, .06);
        line-height: 1.75;
    }
    .metric-card b {
        color: #0f5132;
        font-size: 1.08rem;
    }
    .assist-card {
        min-height: 150px;
        padding: 1rem;
        border-radius: 14px;
        background: #ffffff;
        color: #203125;
        border: 1px solid #dce7d8;
        box-shadow: 0 1px 8px rgba(20, 58, 32, .06);
    }
    .small-muted { color: #5f6f5d; font-size: .9rem; }
    .source-pill {
        display: inline-block;
        padding: .18rem .55rem;
        border-radius: 999px;
        background: #e7f4e4;
        color: #1d5c2f;
        font-size: .78rem;
        border: 1px solid #cfe5ca;
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Namaste! I am AgroAid AI. Ask me about crops, fertilizer, pests, irrigation, weather, schemes, or market prices."
            }
        ]
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = AgroAidChatbot()


def hero():
    st.markdown(
        """
        <div class="hero">
            <h1>🌾 AgroAid AI</h1>
            <p>Intelligent Farmer Assistance Chatbot for crop guidance, pest support, irrigation, schemes, weather and market insights.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def assistance_cards():
    cards = [
        ("🌱 Crop Recommendation", "Soil, season and water-based crop suggestions."),
        ("🧪 Fertilizer Guidance", "Nutrient guidance using crop knowledge base."),
        ("🐛 Pest Management", "Disease symptoms and practical prevention steps."),
        ("💧 Irrigation Advice", "Water-saving irrigation and weather-aware tips."),
        ("🏛️ Govt Schemes", "PM-KISAN, crop insurance, soil card and irrigation schemes."),
        ("📈 Market Guidance", "Sample mandi price trends for major crops."),
        ("☁️ Weather Advice", "Simulated weekly farming weather suggestions."),
        ("♻️ Sustainable Farming", "Organic and soil-friendly farming practices.")
    ]
    cols = st.columns(4)
    for index, (title, text) in enumerate(cards):
        with cols[index % 4]:
            st.markdown(f"<div class='assist-card'><b>{title}</b><p class='small-muted'>{text}</p></div>", unsafe_allow_html=True)


def chatbot_page():
    hero()
    left, right = st.columns([2, 1])

    with right:
        st.subheader("Quick Farmer Questions")
        for query in get_sample_queries():
            if st.button(query, use_container_width=True):
                handle_query(query)
        st.divider()
        use_gemini = st.toggle("Use Gemini API", value=True, help="Uses fallback knowledge base if API key is missing or an error occurs.")
        st.session_state.use_gemini = use_gemini

    with left:
        st.subheader("AI Chatbot")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message.get("source"):
                    st.markdown(f"<span class='source-pill'>{message['source']}</span>", unsafe_allow_html=True)

        prompt = st.chat_input("Ask a farming question...")
        if prompt:
            handle_query(prompt)
            st.rerun()


def handle_query(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response, source = st.session_state.chatbot.get_response(
        prompt,
        st.session_state.messages,
        st.session_state.get("use_gemini", True)
    )
    st.session_state.messages.append({"role": "assistant", "content": response, "source": source})


def recommendations_page():
    hero()
    st.subheader("Smart Recommendations")
    col1, col2, col3 = st.columns(3)
    with col1:
        soil = st.selectbox("Soil type", ["black", "loamy", "alluvial", "red", "sandy loam", "clay"])
    with col2:
        season = st.selectbox("Season", ["kharif", "rabi", "summer", "winter", "monsoon"])
    with col3:
        water = st.selectbox("Water availability", ["Low", "Medium", "High"])

    results = recommend_crops(soil=soil, season=season, water_need=water)
    best_score = results[0]["score"] if results else 0
    if best_score >= 5:
        st.success("Best crop matches for the selected conditions")
    elif best_score > 0:
        st.info("Partial crop matches found. Check the match reasons before choosing.")
    else:
        st.warning("No strong match found, so showing general crop options from the knowledge base.")

    for item in results[:4]:
        crop = item["crop"]
        match_label = "Best match" if item["score"] == best_score and best_score > 0 else "Suggested option"
        st.markdown(
            f"""
            <div class="metric-card">
                <b>{crop['name']}</b> <span class="source-pill">{match_label}</span><br>
                Match reasons: {', '.join(item['reasons'])}<br>
                Soil: {', '.join(crop['soil'])}<br>
                Season: {', '.join(crop['season'])}<br>
                Water need: {crop['water_need']}<br>
                Fertilizers: {', '.join(crop['fertilizers'])}<br>
                Tip: {crop['tips']}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")

    st.divider()
    st.subheader("Instant Guidance")
    tabs = st.tabs(["Fertilizer", "Irrigation", "Pest", "Schemes", "Sustainable"])
    crop_names = [crop["name"] for crop in get_crops()]
    with tabs[0]:
        crop = st.selectbox("Select crop for fertilizer", crop_names)
        st.info(fertilizer_recommendation(crop))
    with tabs[1]:
        crop = st.selectbox("Select crop for irrigation", crop_names, key="irrigation_crop")
        st.info(irrigation_advice(crop))
    with tabs[2]:
        problem = st.text_input("Describe pest or disease symptom", "tomato leaf curl")
        st.warning(pest_guidance(problem))
    with tabs[3]:
        st.write(government_scheme_response())
    with tabs[4]:
        st.write(sustainable_tips())


def analytics_page():
    hero()
    st.subheader("Farming Analytics Dashboard")
    crops = get_crops()
    prices = market_dataframe()
    weather = weather_dataframe()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Crops in KB", len(crops))
    col2.metric("Govt Schemes", len(load_data().get("schemes", [])))
    col3.metric("Market Records", len(prices))
    col4.metric("Weather Days", len(weather))

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("#### Crop Water Need Distribution")
        water_df = crop_count_by_water_need()
        fig, ax = plt.subplots()
        ax.bar(water_df["water_need"], water_df["count"], color=["#2f8f46", "#f2b705", "#1f77b4"])
        ax.set_xlabel("Water Need")
        ax.set_ylabel("Number of Crops")
        ax.set_title("Crop Distribution")
        st.pyplot(fig)

    with chart_col2:
        st.markdown("#### Market Price Guidance")
        fig, ax = plt.subplots()
        ax.bar(prices["crop"], prices["price_per_quintal"], color="#3d7ea6")
        ax.set_xlabel("Crop")
        ax.set_ylabel("Rs. per quintal")
        ax.tick_params(axis="x", rotation=30)
        ax.set_title("Sample Market Prices")
        st.pyplot(fig)

    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        st.markdown("#### Weekly Temperature")
        fig, ax = plt.subplots()
        ax.plot(weather["day"], weather["temperature"], marker="o", color="#d95f02")
        ax.set_ylabel("Temperature C")
        ax.tick_params(axis="x", rotation=30)
        ax.set_title("Weather Simulation")
        st.pyplot(fig)

    with chart_col4:
        st.markdown("#### Rainfall Forecast")
        fig, ax = plt.subplots()
        ax.bar(weather["day"], weather["rainfall"], color="#4c9bd6")
        ax.set_ylabel("Rainfall mm")
        ax.tick_params(axis="x", rotation=30)
        ax.set_title("Rainfall Simulation")
        st.pyplot(fig)

    st.info(weather_advice())
    with st.expander("Soil and Crop Knowledge Table"):
        st.dataframe(crop_distribution_dataframe(), use_container_width=True)


def main():
    initialize_state()
    st.sidebar.title("🌾 AgroAid AI")
    st.sidebar.caption("Social Impact Chatbot Development")
    page = st.sidebar.radio(
        "Navigation",
        ["AI Chatbot", "Recommendations", "Analytics"],
        index=0
    )

    if page == "AI Chatbot":
        chatbot_page()
        st.subheader("Farmer Assistance Modules")
        assistance_cards()
    elif page == "Recommendations":
        recommendations_page()
    elif page == "Analytics":
        analytics_page()


if __name__ == "__main__":
    main()
