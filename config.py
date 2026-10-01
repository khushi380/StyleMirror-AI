import os

# ─── Gemini API ────────────────────────────────────────────────────────────────
# Set your key via Streamlit secrets (secrets.toml) or as an environment variable.
# Do NOT hardcode your API key here — keep it secret!
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-2.5-flash"
GEMINI_VISION_MODEL = "gemini-2.5-flash"

# ─── App Meta ─────────────────────────────────────────────────────────────────
APP_NAME    = "StyleMirror AI"
APP_TAGLINE = "Your AI-Powered Personal Fashion Stylist"
APP_VERSION = "1.0.0"

# ─── Upload Settings ──────────────────────────────────────────────────────────
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_IMAGE_SIZE_MB   = 5

# ─── Style Options ────────────────────────────────────────────────────────────
OCCASIONS = [
    "College", "Interview", "Office", "Wedding", "Party",
    "Festival", "Casual Outing", "Date Night", "Presentation", "Hackathon"
]

SEASONS = ["Summer", "Winter", "Monsoon", "Spring/Autumn"]

BUDGETS = ["₹1,000", "₹3,000", "₹5,000", "₹10,000+", "Custom"]

STYLE_PREFERENCES = [
    "Formal", "Casual", "Streetwear", "Korean",
    "Traditional Indian", "Western", "Luxury", "Minimalist"
]

COLOR_OPTIONS = [
    "Black", "White", "Blue", "Red", "Green",
    "Purple", "Yellow", "Pink", "Beige", "Custom"
]

GENDERS = ["Male", "Female", "Non-binary / Prefer not to say"]

# ─── Face Shapes ──────────────────────────────────────────────────────────────
FACE_SHAPES = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong"]

# ─── Database ─────────────────────────────────────────────────────────────────
DB_PATH = "database/stylemirror.db"
