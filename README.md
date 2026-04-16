# 🧳 Multi-Agent Travel Planner

An intelligent AI-powered travel planning system built with **Google's Agent Development Kit (ADK)** and **Gemini models**. The system uses a multi-agent architecture to search, compare, and optimize travel options across flights, trains, and buses, including smart handling of multi-leg journeys.

---

## 🎯 Project Goal

Build an end-to-end AI travel assistant that:
- **Intelligently searches** for travel options across multiple transportation modes
- **Handles complex scenarios** like cities without airports by calculating multi-leg journeys
- **Optimizes recommendations** based on cost and time
- **Provides actionable insights** in a clean, user-friendly format

---

## 🏗️ Architecture

### **Multi-Agent System Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    travel_assistant                         │
│               (Root Agent - Conversation)                   │
│          Collects: source, destination, date                │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   travel_workflow                           │
│                 (Sequential Agent)                          │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
        ┌─────────────────────────────────┐
        │   STEP 1: travel_planner        │
        │      (Parallel Agent)           │
        └──────────┬──────────────────────┘
                   ├─→ flight_agent  (searches flights via RapidAPI)
                   ├─→ train_agent   (searches trains via IRCTC API)
                   └─→ bus_agent     (generates bus options)
                      ↓
        ┌─────────────────────────────────┐
        │   STEP 2: connection_agent      │
        │   (Multi-leg Journey Planner)   │
        └──────────┬──────────────────────┘
                   │  Detects alternate locations
                   │  Calculates connection options
                   │  (bus, train, taxi to reach alternate airports/stations)
                      ↓
        ┌─────────────────────────────────┐
        │   STEP 3: optimization_agent    │
        │   (Cost & Time Optimizer)       │
        └──────────┬──────────────────────┘
                   │  Compares TOTAL journey costs
                   │  Compares TOTAL journey times
                   │  Recommends: Best for Cost + Best for Time
                      ↓
              Final Output to User
```

### **Key Agents**

| Agent | Type | Purpose | Tools/APIs |
|-------|------|---------|-----------|
| **travel_assistant** | Root | Conversation handler, collects travel details | None |
| **travel_planner** | Parallel | Coordinates simultaneous searches | Sub-agents |
| **flight_agent** | Search | Finds flights, handles nearby airports | RapidAPI Google Flights |
| **train_agent** | Search | Finds trains, handles alternate stations | IRCTC API |
| **bus_agent** | Search | Generates bus options (simulated) | None (future API) |
| **connection_agent** | Analyzer | Calculates multi-leg journey connections | Context analysis |
| **optimization_agent** | Optimizer | Recommends best options by cost & time | get_travel_summary |

### **Data Flow**

1. **User Input** → `travel_assistant` collects source, destination, date
2. **Parallel Search** → All transport agents search simultaneously
   - Each agent stores results with `output_key` in shared state
   - Agents handle alternate locations (nearby airports/stations)
3. **Connection Analysis** → `connection_agent` calculates multi-leg connections
4. **Optimization** → `optimization_agent` retrieves all data, calculates totals, recommends best 2 options
5. **User Output** → Clean, formatted recommendations

---

## 🚀 Features

### **Current Features (Implemented)**

✅ **Multi-modal search**: Flights, trains, buses
✅ **Real-time API integration**: 
   - Google Flights API (via RapidAPI)
   - IRCTC Train API (via RapidAPI)
✅ **Intelligent fallback**: Automatically finds nearby airports/stations
✅ **Multi-leg journey planning**: Calculates connection costs and times
✅ **Smart optimization**: Recommends best options for cost and time
✅ **Clean UX**: Hides intermediate agent chatter, shows only final results

### **Coming Soon (Roadmap)**

🔄 **Enhanced Travel Decision Making**
- Weather-based recommendations
- User preference learning (budget vs comfort)
- Historical price trends
- Cancellation/refund policies

📅 **Calendar Integration**
- Auto-sync bookings to Google Calendar
- Reminder notifications
- Travel itinerary management

💳 **Booking Integration**
- Direct flight/train/bus booking
- Payment gateway integration
- Booking confirmation and e-tickets

🎫 **Additional Features**
- Hotel recommendations near destination
- Local transportation at destination
- Travel insurance suggestions

---

## 🛠️ Technology Stack

- **Framework**: Google Agent Development Kit (ADK) v1.14.0
- **AI Models**: Google Gemini (2.5-pro, 2.5-flash)
- **APIs**: 
  - RapidAPI Google Flights API
  - RapidAPI IRCTC Train API
- **Language**: Python 3.12
- **Async Runtime**: Python AsyncIO
- **Environment Management**: UV (fast Python package manager)

---

## 📦 Installation

### **Prerequisites**
- Python 3.12 or higher
- Google Cloud account (optional, for cloud logging)
- RapidAPI account with subscriptions to:
  - Google Flights API
  - IRCTC Train API

### **Setup Steps**

1. **Clone the repository**
```bash
git clone https://github.com/combfreak45/Multi-Agent-Travel-Planner.git
cd Multi-Agent-Travel-Planner
```

2. **Install UV package manager**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew (macOS)
brew install uv
```

3. **Create virtual environment**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. **Install dependencies**
```bash
uv pip install -r requirements.txt
```

5. **Configure environment variables**

Create a `.env` file in the project root:

```env
# Google AI API Key
GOOGLE_API_KEY=your_google_ai_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE

# Model Configuration
MODEL=gemini-2.5-flash

# RapidAPI Keys
RAPIDAPI_KEY=your_rapidapi_key_here
RAPID_APIKEY_FLIGHT=your_rapidapi_key_here
RAPID_APIKEY_TRAIN=your_rapidapi_key_here
```

**Getting API Keys:**
- **Google AI API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **RapidAPI Keys**: 
  1. Sign up at [RapidAPI](https://rapidapi.com/)
  2. Subscribe to [Google Flights API](https://rapidapi.com/googleflights/api/google-flights2)
  3. Subscribe to [IRCTC API](https://rapidapi.com/irctc/api/irctc-api2)

---

## 🎮 Usage

### **Run the Application**

```bash
source .venv/bin/activate
python main.py
```

### **Example Interaction**

```
Main Agent ready. Type your query (Ctrl+C to exit):

You: Hi
Agent: Hello! I'm here to help you plan your travel. Where are you flying from, 
where are you going, and on what date?

You: I want to travel from Delhi to Mumbai on April 25, 2026
Agent: 
🎯 Travel Recommendations: Delhi to Mumbai

💰 Best for Cost (Total Journey)
- Mode: Train
- Provider/Name: Rajdhani Express
- Total Cost: ₹1,850
- Total Duration: 16 hours
- Journey Details:
  • New Delhi (NDLS) → Mumbai Central (MMCT)
  • Depart: 16:30 | Arrive: 08:30 +1

⚡ Best for Time (Total Journey)
- Mode: Flight
- Provider/Name: IndiGo 6E-123
- Total Cost: ₹4,500
- Total Duration: 2.5 hours
- Journey Details:
  • Delhi (DEL) → Mumbai (BOM)
  • Depart: 09:00 | Arrive: 11:30
```

### **Handling Multi-Leg Journeys**

```
You: I want to travel from Shimla to Mumbai on April 25, 2026
Agent:
🎯 Travel Recommendations: Shimla to Mumbai

💰 Best for Cost (Total Journey)
- Route: Shimla → Chandigarh → Mumbai
- Mode: Multi-leg (Bus + Train)
- Total Cost: ₹2,200 (₹400 bus + ₹1,800 train)
- Total Duration: 20 hours (4hr bus + 16hr train)
- Journey Details:
  • Shimla → Chandigarh: Bus, 4 hours, ₹400
  • Chandigarh → Mumbai: Train, Depart 18:00 → Arrive 10:00 +1

⚡ Best for Time (Total Journey)
- Route: Shimla → Chandigarh → Mumbai
- Mode: Multi-leg (Taxi + Flight)
- Total Cost: ₹7,500 (₹3,000 taxi + ₹4,500 flight)
- Total Duration: 6 hours (3.5hr taxi + 2.5hr flight)
- Journey Details:
  • Shimla → Chandigarh: Taxi, 3.5 hours, ₹3,000
  • Chandigarh (IXC) → Mumbai (BOM): Flight, Depart 14:00 → Arrive 16:30
```

---

## 📂 Project Structure

```
Multi-Agent-Travel-Planner/
├── agents/                      # AI Agent definitions
│   ├── __init__.py
│   ├── flight_agent.py         # Flight search agent
│   ├── train_agent.py          # Train search agent
│   ├── bus_agent.py            # Bus search agent
│   ├── connection_agent.py     # Multi-leg journey analyzer
│   ├── optimization_agent.py   # Cost/time optimizer
│   ├── calendar_agents.py      # (Future) Calendar integration
│   └── system_agents.py        # (Future) Notes and tasks
│
├── tools/                       # Agent tools and utilities
│   ├── __init__.py
│   ├── flight_tools.py         # Flight API integration
│   ├── train_tools.py          # Train API integration
│   ├── get_travel_summary.py   # Aggregate travel data
│   ├── calendar_tools.py       # (Future) Calendar integration
│   └── system_tools.py         # (Future) Notes and tasks
│
├── main.py                      # Application entry point
├── config.py                    # Configuration and environment
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not in git)
├── .gitignore                  # Git ignore rules
└── README.md                    # This file
```

---

## 🧪 Development

### **Enable Debug Mode**

To see all agent outputs (including intermediate steps):

In `main.py`, modify the event filter:
```python
if event.author in ["travel_assistant", "flight_agent", "train_agent", 
                    "bus_agent", "connection_agent", "optimization_agent"]:
```

### **Testing Individual Agents**

Each agent file has commented test code. Uncomment and run:
```bash
python agents/flight_agent.py
```

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

- **combfreak45** - [GitHub](https://github.com/combfreak45)

---

## 🙏 Acknowledgments

- Google Agent Development Kit (ADK) team
- RapidAPI for travel data APIs
- Google Gemini AI models

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/combfreak45/Multi-Agent-Travel-Planner/issues)
- Contact the maintainers

---

**Built with ❤️ using Google ADK and Gemini AI**
