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

## AAT2 Requirement Mapping

### 1. Problem Study & Requirement Analysis

Farmers often face difficulty accessing timely, simple and reliable agricultural advice. The target users include small farmers, marginal farmers, agriculture students and rural support workers. User requirements include simple language, fast responses, crop guidance, fertilizer help, pest management, irrigation support, scheme awareness and market guidance.

### 2. Conversation Design

The chatbot supports intent-based conversation. It identifies whether the farmer is asking about crops, fertilizer, pests, irrigation, schemes, market prices, weather or sustainable farming. Gemini is used for contextual natural language answers, and the local knowledge base provides fallback responses.

### 3. Knowledge Base

The JSON database contains:

- Crop details
- Soil and season suitability
- Fertilizer guidance
- Pest and disease management
- Government agriculture schemes
- Market price samples
- Weather simulation data
- Sustainable farming tips

### 4. System Design

The system uses a modular structure:

- `app.py`: Streamlit UI and dashboard
- `chatbot.py`: Chatbot controller
- `gemini_helper.py`: Gemini API integration
- `database.py`: JSON database access
- `utils.py`: Recommendation and fallback logic
- `farmer_data.json`: Agriculture knowledge base

### 5. Implementation

The implementation uses clean Python functions, reusable modules, error handling and session-based chat memory. The UI includes chatbot, recommendations, analytics and project report sections.

### 6. Testing

Use the sample queries in the app to test:

| Query | Expected Result |
|---|---|
| Which crop is suitable for black soil? | Cotton, wheat or other black soil crops |
| Best fertilizer for rice? | Urea, DAP, MOP and soil-test note |
| How to prevent tomato leaf disease? | Leaf curl prevention and whitefly control |
| Government schemes for farmers? | PM-KISAN, Fasal Bima, Soil Health Card |
| How to reduce water usage? | Drip irrigation, mulching and sprinkler advice |

## Screenshots

Add screenshots here after running the app:

- Home chatbot screen
- Recommendations page
- Analytics dashboard
- AAT2 report page

## Data Visualization

The dashboard includes:

- Crop water need distribution chart
- Market price chart
- Weekly temperature chart
- Rainfall forecast chart
- Soil and crop knowledge table

## AI Concepts Used

- Natural language processing
- Prompt engineering
- Contextual conversation memory
- Intent detection
- Knowledge-base retrieval
- Fallback response generation
- Recommendation engine

## Benefits

- Helps farmers access understandable agriculture guidance
- Supports awareness of government schemes
- Encourages sustainable and water-saving farming
- Useful for college demonstration and social impact discussion
- Works even without Gemini API through fallback responses

## Limitations

- Weather data is simulated
- Market prices are sample values and should be verified from live mandi sources
- Pest guidance is advisory and not a replacement for expert field inspection
- Gemini requires an internet connection and valid API key

## Future Improvements

- Add live weather API integration
- Add real-time mandi price API
- Add multilingual support for local languages
- Add voice input and output
- Add image-based pest detection
- Add SQLite database and admin panel
- Add farmer profile-based personalized recommendations

## College Submission Use

This project is suitable for:

- AAT2 project demonstration
- PPT presentation
- Report/PDF generation
- Live Streamlit demo
- Social impact chatbot evaluation
