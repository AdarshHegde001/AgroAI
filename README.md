# AgroAid AI – Intelligent Farmer Assistance Chatbot

AgroAid AI is a full-stack AI-powered social impact chatbot built for the AAT2 Social Impact Chatbot Development project. It helps farmers get simple guidance about crop selection, fertilizer use, pest management, irrigation, weather-based advice, government agriculture schemes, market prices and sustainable farming practices.

## Project Objective

The objective is to develop a user-friendly AI chatbot that supports farmers with practical agriculture information. The system combines a local agriculture knowledge base with Gemini API integration and intelligent fallback responses, so the chatbot can still answer useful questions even when the API is unavailable.

## Features

- Conversational farmer assistance chatbot
- Gemini API integration using `from google import genai`
- Model: `gemini-2.5-flash-lite`
- Knowledge-base fallback responses
- Crop recommendation by soil, season and water availability
- Fertilizer recommendation
- Pest and disease management guidance
- Irrigation and water-saving advice
- Weather simulation module
- Government scheme guidance
- Sample market price guidance
- Sustainable and organic farming tips
- Chatbot memory/history
- Modern Streamlit dashboard
- Matplotlib charts for farming analytics
- AAT2 report-ready documentation page

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| AI | Gemini API, `google-genai` |
| Database | JSON |
| Visualization | Matplotlib |
| Data Handling | Pandas |

## Project Structure

```text
farmer-chatbot/
├── app.py
├── chatbot.py
├── gemini_helper.py
├── database.py
├── utils.py
├── requirements.txt
├── README.md
└── data/
    └── farmer_data.json
```

## Architecture

```text
Farmer/User
   ↓
Streamlit Dashboard
   ↓
AgroAid Chatbot Controller
   ↓
Intent Detection + Knowledge Base
   ↓
Gemini API if available
   ↓
Fallback Recommendation Engine if Gemini fails
   ↓
Simple farmer-friendly response
```

## Chatbot Workflow

1. User asks a farming question in the Streamlit chatbot.
2. The chatbot stores the query in session history.
3. The system sends the query and recent context to Gemini.
4. If Gemini returns a response, it is shown to the user.
5. If Gemini fails or no API key is configured, the local knowledge-base fallback is used.
6. The response is displayed with its source.

## Installation

```bash
cd farmer-chatbot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
cd farmer-chatbot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Gemini API Setup

Set your Gemini API key before running the app:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

The app also supports `GOOGLE_API_KEY`.

## How to Run

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Sample Queries

- Which crop is suitable for black soil?
- Best fertilizer for rice?
- How to prevent tomato leaf disease?
- What government schemes are available for farmers?
- How to reduce water usage in farming?
- What crop should I grow during summer?
- Market price of wheat?
- Organic farming tips?




