# 🧭 Travel Itinerary Generator

A modern AI-powered **Travel Itinerary Generator** built with [Agno](https://pypi.org/project/agno/), [Groq](https://groq.com/), and [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/).  
This project comes in two flavors:

- **CLI Version (`main.py`)** → Run locally in your terminal  
- **Web App (`app.py`)** → A minimal [Streamlit](https://travel-itinerary-generator-agno-2ftqxnrgvv3jb4ltpgemnu.streamlit.app/) app with a clean UI
<img width="1910" height="933" alt="image" src="https://github.com/user-attachments/assets/3d837f57-41fb-4f73-a4c9-c4ff53bd213f" />


---

## ✨ Features

- Generates a **day-wise travel itinerary** based on:
  - Destination country or city
  - Budget (USD/INR/any currency)
  - Duration of stay (days)
  - Optional interests (history, food, beaches, nightlife, etc.)
- Integrates **DuckDuckGo Search** to fetch up-to-date highlights  
- Budget-aware recommendations with food, activities, and cultural spots  
- Two modes:
  - **CLI** → quick, terminal-based  
  - **Streamlit** → modern UI (web version)

---

## 🛠️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/travel-itinerary-generator.git
cd travel-itinerary-generator

# Install with pip
pip install -r requirements.txt

# OR with poetry
poetry install
```

Create a `.env` file in the root directory with your API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🚀 CLI Version (`main.py`)

The CLI version is the simplest way to use the itinerary generator directly from your terminal.

### ▶️ Run

```bash
python main.py
```

The script will use your Groq model + DuckDuckGo integration to generate a detailed itinerary.

### 💬 Example Prompt

```text
I want to travel to Italy with a budget of 2000 USD for 5 days. Can you help me plan my trip?
```

### 📝 Example Output (Markdown-formatted)

```markdown
### Day 1: Rome
- Morning: Visit the Colosseum
- Afternoon: Explore the Roman Forum
- Evening: Enjoy Carbonara at a local trattoria

### Day 2: Florence
- Morning: Train to Florence
- Afternoon: Visit the Uffizi Gallery
- Evening: Try Bistecca alla Fiorentina

### Day 3: Venice
- Morning: Gondola ride in the canals
- Afternoon: St. Mark’s Basilica
- Evening: Fresh seafood risotto
```

---

## 🌐 Streamlit App (`app.py`)

The project also includes a modern Streamlit app for a more interactive experience.

👉 Access it here: **[URL]**

*(URL will be added once hosting is live.)*

---

## 📂 Project Structure

```
├── app.py          # Streamlit web app
├── main.py         # CLI app
├── requirements.txt
├── README.md
└── .env.example    # Example env file
```

---

## ⚙️ Tech Stack

- **Python 3.10+**
- [Agno](https://pypi.org/project/agno/) – Multi-agent orchestration  
- [Groq](https://groq.com/) – LLM inference  
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) – Real-time web search  
- [Streamlit](https://streamlit.io/) – Modern UI

---

## 📌 Notes

- Make sure you have a valid **GROQ API Key** set in `.env`.  
- The **CLI version** is better for debugging and quick testing.  
- The **Streamlit version** is optimized for clean Markdown outputs.  
- The **DuckDuckGo search wrapper** has been patched to handle type mismatches (`max_results` bug).

---

## 🧑‍💻 Contributing

PRs and issues are welcome!  
Fork the repo and send improvements — whether for itinerary formatting, UI polish, or agent logic.

---

## 📜 License

MIT License — feel free to use and modify.
