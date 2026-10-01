import streamlit as st

def section_header(icon: str, title: str):
    st.markdown(f"""
    <div class="sm-section-header">
        <div class="sm-section-icon">{icon}</div>
        <div class="sm-section-title">{title}</div>
    </div>""", unsafe_allow_html=True)

def outfit_item(emoji: str, label: str, value: str):
    st.markdown(f"""
    <div class="sm-outfit-item">
        <div class="sm-outfit-emoji">{emoji}</div>
        <div>
            <div class="sm-outfit-label">{label}</div>
            <div class="sm-outfit-value">{value}</div>
        </div>
    </div>""", unsafe_allow_html=True)

def badge(text: str, variant: str = "purple"):
    st.markdown(f'<span class="sm-badge sm-badge-{variant}">{text}</span>', unsafe_allow_html=True)

def face_result_card(face_shape: str, confidence: int, skin_tone: str, undertone: str):
    st.markdown(f"""
    <div class="sm-face-result">
        <div style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:var(--text-muted);margin-bottom:8px;">FACE SHAPE DETECTED</div>
        <div class="sm-face-shape-name">{face_shape}</div>
        <div style="font-size:0.82rem;color:var(--text-muted);margin-top:6px;">
            {skin_tone} Skin · {undertone} Undertone
        </div>
        <div class="sm-confidence-bar">
            <div class="sm-confidence-fill" style="width:{confidence}%"></div>
        </div>
        <div style="font-size:0.72rem;color:var(--text-muted);margin-top:6px;">
            {confidence}% Confidence
        </div>
    </div>""", unsafe_allow_html=True)

def score_display(current: float, potential: float, archetype: str):
    cur_pct  = int((current / 10) * 360)
    st.markdown(f"""
    <div style="text-align:center;padding:20px;">
        <div style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:var(--text-muted);margin-bottom:16px;">FASHION SCORE</div>
        <div style="display:flex;justify-content:center;gap:32px;flex-wrap:wrap;">
            <div>
                <div class="sm-score-circle" style="background:conic-gradient(
                    var(--accent-purple) 0deg {cur_pct}deg,
                    var(--bg-hover) {cur_pct}deg 360deg);">
                    <div class="sm-score-inner">
                        <div class="sm-score-number">{current}</div>
                        <div class="sm-score-label">NOW</div>
                    </div>
                </div>
                <div style="font-size:0.78rem;color:var(--text-muted)">Current</div>
            </div>
            <div>
                <div class="sm-score-circle" style="background:conic-gradient(
                    var(--accent-gold) 0deg {int((potential/10)*360)}deg,
                    var(--bg-hover) {int((potential/10)*360)}deg 360deg);">
                    <div class="sm-score-inner">
                        <div class="sm-score-number">{potential}</div>
                        <div class="sm-score-label">POTENTIAL</div>
                    </div>
                </div>
                <div style="font-size:0.78rem;color:var(--text-muted)">With Tips</div>
            </div>
        </div>
        <div style="margin-top:16px;">
            <span class="sm-badge sm-badge-purple">✦ {archetype}</span>
        </div>
    </div>""", unsafe_allow_html=True)

def color_palette_display(colors: list):
    swatches = ""
    for c in colors:
        hex_val = c.get("hex", "") if isinstance(c, dict) else ""
        name    = c.get("name", str(c)) if isinstance(c, dict) else str(c)
        reason  = c.get("reason", "") if isinstance(c, dict) else ""

        # Ensure hex_val is a valid colour; fall back to a visible grey
        if not hex_val or not hex_val.startswith("#"):
            hex_val = "#888888"

        swatches += f"""
        <div style="display:inline-block;text-align:center;margin:8px;">
            <div style="
                width:56px;
                height:56px;
                border-radius:12px;
                background-color:{hex_val};
                border:2px solid rgba(255,255,255,0.15);
                cursor:pointer;
                transition:transform 0.2s;
                box-shadow:0 2px 8px rgba(0,0,0,0.4);
                display:block;"
                 title="{name}: {reason}">
            </div>
            <div style="font-size:0.65rem;color:#9CA3AF;margin-top:6px;
                        max-width:60px;word-break:break-word;line-height:1.3;"
            >{name}</div>
            <div style="font-size:0.6rem;color:#6B7280;margin-top:2px;"
            >{hex_val}</div>
        </div>"""
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:4px;">{swatches}</div>',
        unsafe_allow_html=True
    )

def stat_box(value: str, label: str):
    return f"""
    <div class="sm-stat-box">
        <div class="sm-stat-value">{value}</div>
        <div class="sm-stat-label">{label}</div>
    </div>"""

def trend_card(name: str, description: str, tip: str):
    st.markdown(f"""
    <div class="sm-trend-card">
        <div style="font-weight:600;color:var(--text-primary);margin-bottom:6px;
                    padding-left:8px;">{name}</div>
        <div style="font-size:0.85rem;color:var(--text-secondary);
                    margin-bottom:8px;padding-left:8px;">{description}</div>
        <div style="font-size:0.78rem;color:var(--accent-purple-light);
                    padding-left:8px;">💡 {tip}</div>
    </div>""", unsafe_allow_html=True)

def chat_message(role: str, content: str):
    if role == "user":
        st.markdown(f"""
        <div class="sm-chat-msg user">
            <div class="sm-chat-avatar user">👤</div>
            <div class="sm-chat-bubble user">{content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="sm-chat-msg">
            <div class="sm-chat-avatar ai">✦</div>
            <div class="sm-chat-bubble ai">{content}</div>
        </div>""", unsafe_allow_html=True)

def step_item(num: int, title: str, text: str):
    st.markdown(f"""
    <div class="sm-step">
        <div class="sm-step-num">{num}</div>
        <div>
            <div class="sm-step-title">{title}</div>
            <div class="sm-step-text">{text}</div>
        </div>
    </div>""", unsafe_allow_html=True)
