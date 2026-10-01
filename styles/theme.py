DARK_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-primary:    #0A0A0F;
    --bg-secondary:  #12121A;
    --bg-card:       #1A1A26;
    --bg-hover:      #22223A;
    --accent-purple: #9333EA;
    --accent-gold:   #D4AF37;
    --accent-purple-light: #C084FC;
    --text-primary:  #F8F8FF;
    --text-secondary:#B0B0CC;
    --text-muted:    #6B6B8A;
    --border:        #2A2A40;
    --border-accent: #9333EA44;
    --success:       #22C55E;
    --warning:       #F59E0B;
    --error:         #EF4444;
    --gradient-1: linear-gradient(135deg, #9333EA, #D4AF37);
    --gradient-2: linear-gradient(135deg, #1A1A26, #2A1A3E);
    --shadow: 0 8px 32px rgba(147, 51, 234, 0.15);
}

/* ── Reset & Base ─────────────────────── */
* { box-sizing: border-box; }

.stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit Default Chrome ───── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top Bar ──────────────────────────── */
.sm-topbar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: 12px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(12px);
}
.sm-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.05em;
}
.sm-logo-sub {
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: -2px;
}

/* ── Hero Section ────────────────────── */
.sm-hero {
    text-align: center;
    padding: 64px 24px 48px;
    position: relative;
    overflow: hidden;
}
.sm-hero::before {
    content: '';
    position: absolute;
    top: -100px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(147,51,234,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.sm-hero-eyebrow {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent-purple-light);
    margin-bottom: 16px;
    font-weight: 500;
}
.sm-hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 700;
    line-height: 1.15;
    margin: 0 0 20px;
    color: var(--text-primary);
}
.sm-hero-title span {
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sm-hero-sub {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto 36px;
    line-height: 1.7;
    font-weight: 300;
}

/* ── Cards ────────────────────────────── */
.sm-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.sm-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow);
}
.sm-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.sm-card-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 16px;
}

/* ── Section Headers ─────────────────── */
.sm-section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.sm-section-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--gradient-2);
    border: 1px solid var(--border-accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}
.sm-section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

/* ── Badges ────────────────────────────── */
.sm-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.05em;
}
.sm-badge-purple {
    background: rgba(147, 51, 234, 0.2);
    color: var(--accent-purple-light);
    border: 1px solid rgba(147, 51, 234, 0.4);
}
.sm-badge-gold {
    background: rgba(212, 175, 55, 0.15);
    color: var(--accent-gold);
    border: 1px solid rgba(212, 175, 55, 0.3);
}
.sm-badge-green {
    background: rgba(34, 197, 94, 0.15);
    color: #4ADE80;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

/* ── Face Shape Display ──────────────── */
.sm-face-result {
    text-align: center;
    padding: 28px;
    background: var(--gradient-2);
    border: 1px solid var(--border-accent);
    border-radius: 16px;
}
.sm-face-shape-name {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sm-confidence-bar {
    width: 100%;
    height: 6px;
    background: var(--bg-hover);
    border-radius: 3px;
    margin-top: 12px;
    overflow: hidden;
}
.sm-confidence-fill {
    height: 100%;
    border-radius: 3px;
    background: var(--gradient-1);
    transition: width 1s ease;
}

/* ── Score Gauge ─────────────────────── */
.sm-score-circle {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: conic-gradient(var(--accent-purple) 0%, var(--accent-gold) 60%, var(--bg-hover) 60%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    position: relative;
}
.sm-score-inner {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--bg-card);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
.sm-score-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.sm-score-label {
    font-size: 0.55rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Color Swatches ──────────────────── */
.sm-color-swatch {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: inline-block;
    border: 2px solid var(--border);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    margin: 4px;
}
.sm-color-swatch:hover {
    transform: scale(1.15);
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

/* ── Outfit Cards ────────────────────── */
.sm-outfit-item {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    transition: border-color 0.2s;
}
.sm-outfit-item:hover { border-color: var(--border-accent); }
.sm-outfit-emoji {
    font-size: 1.6rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.sm-outfit-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-purple-light);
    margin-bottom: 4px;
}
.sm-outfit-value {
    font-size: 0.92rem;
    color: var(--text-primary);
    line-height: 1.5;
}

/* ── Chatbot ─────────────────────────── */
.sm-chat-container {
    height: 420px;
    overflow-y: auto;
    padding: 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px 16px 0 0;
    scroll-behavior: smooth;
}
.sm-chat-msg {
    margin-bottom: 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.sm-chat-msg.user { flex-direction: row-reverse; }
.sm-chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.sm-chat-avatar.ai {
    background: var(--gradient-1);
    color: white;
}
.sm-chat-avatar.user {
    background: var(--bg-hover);
    color: var(--text-secondary);
}
.sm-chat-bubble {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 0.88rem;
    line-height: 1.6;
}
.sm-chat-bubble.ai {
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-primary);
    border-radius: 4px 16px 16px 16px;
}
.sm-chat-bubble.user {
    background: linear-gradient(135deg, #9333EA, #7C3AED);
    color: white;
    border-radius: 16px 4px 16px 16px;
}

/* ── Report ──────────────────────────── */
.sm-report {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    line-height: 1.9;
    color: var(--text-secondary);
    font-size: 0.92rem;
}
.sm-report h2 {
    font-family: 'Playfair Display', serif;
    color: var(--text-primary);
    font-size: 1.15rem;
    margin: 24px 0 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border-accent);
}
.sm-report h2:first-child { margin-top: 0; }
.sm-report strong { color: var(--text-primary); }

/* ── Steps / Progress ────────────────── */
.sm-step {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px;
    background: var(--bg-card);
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid var(--border);
}
.sm-step-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--gradient-1);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.sm-step-text {
    font-size: 0.88rem;
    color: var(--text-secondary);
}
.sm-step-title {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.92rem;
    margin-bottom: 2px;
}

/* ── Feature Pills ───────────────────── */
.sm-feature-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 20px 0;
}
.sm-feature-pill {
    padding: 8px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 24px;
    font-size: 0.8rem;
    color: var(--text-secondary);
    transition: all 0.2s;
}
.sm-feature-pill:hover {
    border-color: var(--accent-purple);
    color: var(--accent-purple-light);
}

/* ── Trend Cards ─────────────────────── */
.sm-trend-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}
.sm-trend-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px;
    height: 100%;
    background: var(--gradient-1);
}

/* ── Upload Zone ─────────────────────── */
.sm-upload-hint {
    text-align: center;
    padding: 20px;
    background: var(--bg-card);
    border: 2px dashed var(--border-accent);
    border-radius: 16px;
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 12px;
}

/* ── Stats Row ───────────────────────── */
.sm-stats-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.sm-stat-box {
    flex: 1;
    min-width: 120px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
}
.sm-stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sm-stat-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
}

.stButton > button[kind="primary"] {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 15px rgba(147, 51, 234, 0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(147, 51, 234, 0.55) !important;
    opacity: 0.95 !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(1px) !important;
}

.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.04) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 10px 24px !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.03em !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    color: var(--text-primary) !important;
    border-color: var(--accent-purple-light) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"]:active {
    transform: translateY(1px) !important;
}

/* Fallback for general buttons if kind is unspecified */
.stButton > button:not([kind]) {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 15px rgba(147, 51, 234, 0.25) !important;
}
.stButton > button:not([kind]):hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(147, 51, 234, 0.45) !important;
    opacity: 0.95 !important;
}

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
div[data-testid="stSidebarUserContent"],
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #130a24 0%, #0a0a0f 100%) !important;
    border-right: 1px solid rgba(147, 51, 234, 0.3) !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 2px rgba(147,51,234,0.2) !important;
}

label, .stRadio label, .stCheckbox label {
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
}

.stMarkdown p, .stMarkdown li {
    color: var(--text-secondary) !important;
    line-height: 1.8 !important;
}

.stInfo {
    background: rgba(147, 51, 234, 0.1) !important;
    border: 1px solid rgba(147, 51, 234, 0.3) !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
}
.stSuccess {
    background: rgba(34, 197, 94, 0.1) !important;
    border: 1px solid rgba(34, 197, 94, 0.3) !important;
    border-radius: 10px !important;
}
.stWarning {
    background: rgba(245, 158, 11, 0.1) !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 10px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0 8px !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-purple-light) !important;
    border-bottom: 2px solid var(--accent-purple) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding-top: 24px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-purple); }

/* Spinner */
.stSpinner > div { border-top-color: var(--accent-purple) !important; }

/* Divider */
hr { border-color: var(--border) !important; opacity: 1 !important; }
</style>
"""

LIGHT_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-primary:    #FAFAFA;
    --bg-secondary:  #FFFFFF;
    --bg-card:       #F4F4F8;
    --bg-hover:      #EEEEF4;
    --accent-purple: #7C3AED;
    --accent-gold:   #B8860B;
    --accent-purple-light: #6D28D9;
    --text-primary:  #0F0F1A;
    --text-secondary:#3D3D5C;
    --text-muted:    #8080A0;
    --border:        #E0E0EC;
    --border-accent: #7C3AED44;
    --success:       #16A34A;
    --warning:       #D97706;
    --error:         #DC2626;
    --gradient-1: linear-gradient(135deg, #7C3AED, #B8860B);
    --gradient-2: linear-gradient(135deg, #F4F0FF, #FFF8E7);
    --shadow: 0 8px 32px rgba(124, 58, 237, 0.12);
}

* { box-sizing: border-box; }

.stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.sm-topbar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: 12px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.sm-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.05em;
}
.sm-logo-sub {
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: -2px;
}

.sm-hero {
    text-align: center;
    padding: 64px 24px 48px;
    position: relative;
    overflow: hidden;
}
.sm-hero::before {
    content: '';
    position: absolute;
    top: -100px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(124,58,237,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.sm-hero-eyebrow {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent-purple-light);
    margin-bottom: 16px;
    font-weight: 500;
}
.sm-hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 700;
    line-height: 1.15;
    margin: 0 0 20px;
    color: var(--text-primary);
}
.sm-hero-title span {
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sm-hero-sub {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto 36px;
    line-height: 1.7;
    font-weight: 300;
}

.sm-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.sm-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow);
}
.sm-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.sm-card-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.sm-section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.sm-section-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--gradient-2);
    border: 1px solid var(--border-accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}
.sm-section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.sm-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.05em;
}
.sm-badge-purple {
    background: rgba(124, 58, 237, 0.1);
    color: var(--accent-purple-light);
    border: 1px solid rgba(124, 58, 237, 0.3);
}
.sm-badge-gold {
    background: rgba(184, 134, 11, 0.1);
    color: var(--accent-gold);
    border: 1px solid rgba(184, 134, 11, 0.3);
}
.sm-badge-green {
    background: rgba(22, 163, 74, 0.1);
    color: var(--success);
    border: 1px solid rgba(22, 163, 74, 0.3);
}

.sm-face-result {
    text-align: center;
    padding: 28px;
    background: var(--gradient-2);
    border: 1px solid var(--border-accent);
    border-radius: 16px;
}
.sm-face-shape-name {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sm-confidence-bar {
    width: 100%;
    height: 6px;
    background: var(--bg-hover);
    border-radius: 3px;
    margin-top: 12px;
    overflow: hidden;
}
.sm-confidence-fill {
    height: 100%;
    border-radius: 3px;
    background: var(--gradient-1);
}

.sm-score-circle {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: conic-gradient(#7C3AED 0%, #B8860B 60%, var(--bg-hover) 60%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    position: relative;
}
.sm-score-inner {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--bg-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
.sm-score-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.sm-score-label {
    font-size: 0.55rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.sm-color-swatch {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: inline-block;
    border: 2px solid var(--border);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    margin: 4px;
}
.sm-color-swatch:hover {
    transform: scale(1.15);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.sm-outfit-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    transition: border-color 0.2s;
}
.sm-outfit-item:hover { border-color: var(--border-accent); }
.sm-outfit-emoji { font-size: 1.6rem; flex-shrink: 0; margin-top: 2px; }
.sm-outfit-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-purple-light);
    margin-bottom: 4px;
}
.sm-outfit-value { font-size: 0.92rem; color: var(--text-primary); line-height: 1.5; }

.sm-chat-container {
    height: 420px;
    overflow-y: auto;
    padding: 16px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px 16px 0 0;
    scroll-behavior: smooth;
}
.sm-chat-msg { margin-bottom: 16px; display: flex; align-items: flex-start; gap: 10px; }
.sm-chat-msg.user { flex-direction: row-reverse; }
.sm-chat-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0;
}
.sm-chat-avatar.ai { background: var(--gradient-1); color: white; }
.sm-chat-avatar.user { background: var(--bg-hover); color: var(--text-secondary); }
.sm-chat-bubble {
    max-width: 75%; padding: 12px 16px; border-radius: 16px;
    font-size: 0.88rem; line-height: 1.6;
}
.sm-chat-bubble.ai {
    background: var(--bg-secondary); border: 1px solid var(--border);
    color: var(--text-primary); border-radius: 4px 16px 16px 16px;
}
.sm-chat-bubble.user {
    background: linear-gradient(135deg, #7C3AED, #6D28D9);
    color: white; border-radius: 16px 4px 16px 16px;
}

.sm-report {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    line-height: 1.9;
    color: var(--text-secondary);
    font-size: 0.92rem;
}
.sm-report h2 {
    font-family: 'Playfair Display', serif;
    color: var(--text-primary);
    font-size: 1.15rem;
    margin: 24px 0 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border-accent);
}
.sm-report h2:first-child { margin-top: 0; }
.sm-report strong { color: var(--text-primary); }

.sm-step {
    display: flex; align-items: center; gap: 14px;
    padding: 16px; background: var(--bg-secondary);
    border-radius: 12px; margin-bottom: 10px;
    border: 1px solid var(--border);
}
.sm-step-num {
    width: 32px; height: 32px; border-radius: 50%;
    background: var(--gradient-1); color: white;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem; flex-shrink: 0;
}
.sm-step-text { font-size: 0.88rem; color: var(--text-secondary); }
.sm-step-title { font-weight: 600; color: var(--text-primary); font-size: 0.92rem; margin-bottom: 2px; }

.sm-feature-grid { display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }
.sm-feature-pill {
    padding: 8px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 24px;
    font-size: 0.8rem;
    color: var(--text-secondary);
    transition: all 0.2s;
}
.sm-feature-pill:hover { border-color: var(--accent-purple); color: var(--accent-purple-light); }

.sm-trend-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}
.sm-trend-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; width: 3px; height: 100%;
    background: var(--gradient-1);
}

.sm-upload-hint {
    text-align: center; padding: 20px;
    background: var(--bg-secondary);
    border: 2px dashed var(--border-accent);
    border-radius: 16px; color: var(--text-muted);
    font-size: 0.85rem; margin-top: 12px;
}

.sm-stats-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.sm-stat-box {
    flex: 1; min-width: 120px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 16px; text-align: center;
}
.sm-stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem; font-weight: 700;
    background: var(--gradient-1);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sm-stat-label {
    font-size: 0.7rem; color: var(--text-muted);
    letter-spacing: 0.1em; text-transform: uppercase; margin-top: 4px;
}

.stButton > button[kind="primary"] {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.45) !important;
    opacity: 0.95 !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(1px) !important;
}

.stButton > button[kind="secondary"] {
    background: rgba(0, 0, 0, 0.03) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 10px 24px !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.03em !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(0, 0, 0, 0.06) !important;
    color: var(--text-primary) !important;
    border-color: var(--accent-purple-light) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"]:active {
    transform: translateY(1px) !important;
}

/* Fallback for general buttons if kind is unspecified */
.stButton > button:not([kind]) {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2) !important;
}
.stButton > button:not([kind]):hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35) !important;
    opacity: 0.95 !important;
}

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
div[data-testid="stSidebarUserContent"],
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f5 0%, #fafafa 100%) !important;
    border-right: 1px solid rgba(124, 58, 237, 0.15) !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}

label, .stRadio label, .stCheckbox label {
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
}
.stMarkdown p, .stMarkdown li {
    color: var(--text-secondary) !important;
    line-height: 1.8 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] { color: var(--text-muted) !important; font-size: 0.85rem !important; }
.stTabs [aria-selected="true"] {
    color: var(--accent-purple-light) !important;
    border-bottom: 2px solid var(--accent-purple) !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-purple); }

hr { border-color: var(--border) !important; opacity: 1 !important; }
</style>
"""
