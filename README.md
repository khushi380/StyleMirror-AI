# ✦ StyleMirror AI
### AI-Powered Personalized Fashion Recommendation & Virtual Styling Assistant

---

## 🚀 Quick Setup

### 1. Clone / Download the project
```bash
git clone <your-repo>
cd stylemirror
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API Key
Get a free API key from: https://aistudio.google.com/app/apikey

**Local (create `.streamlit/secrets.toml`):**
```toml
GEMINI_API_KEY = "your_key_here"
```

**OR set as environment variable:**
```bash
export GEMINI_API_KEY="your_key_here"
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy Free on Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo → select `app.py`
4. In **Secrets**, add:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
5. Deploy!

---

## 📁 Project Structure

```
stylemirror/
├── app.py                    ← Main Streamlit app (all pages)
├── config.py                 ← App settings & constants
├── requirements.txt          ← Python dependencies
├── README.md
│
├── fashion_engine/
│   └── gemini_engine.py      ← All Gemini AI calls (10 functions)
│
├── face_analysis/
│   └── image_processor.py    ← OpenCV image preprocessing
│
├── styles/
│   └── theme.py              ← Dark & Light CSS themes
│
├── utils/
│   └── components.py         ← Reusable UI components
│
├── database/
│   └── db.py                 ← SQLite helpers
│
└── .streamlit/
    └── secrets.toml          ← API keys (not committed to git)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| Face Shape Analysis | AI detects face shape + skin tone + confidence score |
| Outfit Recommendations | Complete look for occasion, season, budget |
| Hairstyle Suggestions | Face-shape-aware hairstyle guide |
| Makeup & Grooming | Full beauty guide for any occasion |
| Accessory Pairing | Watch, jewelry, bag, eyewear recommendations |
| Color Palette | Personal color season + primary/accent colors |
| Fashion Score | Current + potential score with breakdown |
| Style Report | 400-word personalized style summary |
| Trend Explorer | Season & gender-specific trends |
| AI Chatbot | Fashion Q&A with context from your analysis |
| Saved Looks | Gallery with full report history |
| Dark/Light Theme | Toggle with full theme support |

---

## 🔑 API Used

- **Google Gemini 1.5 Flash** — Free tier, handles all AI features
  - Get key: https://aistudio.google.com/app/apikey
  - Free quota: 15 RPM, 1M TPM, 1500 requests/day

---

## 📝 Notes

- No custom model training required
- No dataset collection required
- Completely free tech stack
- SQLite data is session-local on Streamlit Cloud (resets on restart)
- For persistent storage, replace SQLite with a free DB like Supabase
