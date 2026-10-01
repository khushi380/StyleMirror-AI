import streamlit as st
import uuid
import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image
from styles.theme import DARK_THEME_CSS, LIGHT_THEME_CSS
from config import (APP_NAME, OCCASIONS, SEASONS, BUDGETS,
                    STYLE_PREFERENCES, COLOR_OPTIONS, GENDERS)
from database.db import (init_db, save_look, get_saved_looks,
                          delete_look, save_chat_message, get_chat_history)
from fashion_engine.gemini_engine import (
    analyze_face, get_outfit_recommendation, get_hairstyle_recommendation,
    get_makeup_recommendation, get_accessory_recommendation,
    get_color_palette, get_fashion_score, get_full_style_report,
    get_fashion_trends, fashion_chat
)
from face_analysis.image_processor import preprocess_image, detect_face_opencv
from utils.components import (section_header, outfit_item, face_result_card,
                               score_display, color_palette_display, trend_card,
                               chat_message, step_item, stat_box, badge)
import json

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StyleMirror AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Init ──────────────────────────────────────────────────────────────────────
init_db()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "face_data" not in st.session_state:
    st.session_state.face_data = {}
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "all_results" not in st.session_state:
    st.session_state.all_results = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── Theme CSS ─────────────────────────────────────────────────────────────────
css = DARK_THEME_CSS if st.session_state.theme == "dark" else LIGHT_THEME_CSS
st.markdown(css, unsafe_allow_html=True)

# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 8px;">
        <div class="sm-logo">✦ StyleMirror</div>
        <div class="sm-logo-sub">AI Fashion Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    pages = {
        "🏠  Home":            "home",
        "📸  Upload & Analyze": "upload",
        "👗  Outfit Recs":      "outfit",
        "💇  Hairstyle":        "hair",
        "💄  Makeup & Grooming":"makeup",
        "💍  Accessories":      "accessories",
        "🎨  Color Palette":    "colors",
        "⭐  Fashion Score":    "score",
        "📋  Style Report":     "report",
        "🔥  Trend Explorer":   "trends",
        "💬  AI Chatbot":       "chatbot",
        "🗂️  Saved Looks":      "saved",
        "ℹ️  About":            "about",
    }

    for label, page_key in pages.items():
        is_active = st.session_state.page == page_key
        if st.button(
            label,
            key=f"nav_{page_key}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = page_key
            st.rerun()
    st.divider()

    # ── Gemini API Key Input ──────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:0.72rem;color:var(--text-muted);
                letter-spacing:0.1em;text-transform:uppercase;
                margin-bottom:6px;">🔑 Gemini API Key</div>
    """, unsafe_allow_html=True)

    user_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.get("user_gemini_api_key", ""),
        type="password",
        placeholder="AIzaSy...",
        label_visibility="collapsed",
        key="api_key_input_field"
    )
    if user_key_input != st.session_state.get("user_gemini_api_key", ""):
        st.session_state.user_gemini_api_key = user_key_input
        st.session_state.api_key_validated = False
        st.rerun()

    # Determine effective key for status display
    from config import GEMINI_API_KEY as _cfg_key
    _effective_key = st.session_state.get("user_gemini_api_key", "") or _cfg_key or ""
    _key_ok = bool(_effective_key and _effective_key not in ("", "PASTE_YOUR_KEY_HERE", "your_gemini_api_key_here") and _effective_key.strip())

    if _key_ok:
        st.markdown("""
        <div style="font-size:0.75rem;color:#4ade80;margin-top:4px;">
            ✅ AI Mode Active
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:0.72rem;color:var(--text-muted);margin-top:4px;line-height:1.5;">
            🎭 Demo Mode — get a free key at<br>
            <a href="https://aistudio.google.com/app/apikey" target="_blank"
               style="color:var(--accent-gold);">aistudio.google.com</a>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Theme toggle
    theme_label = "☀️ Light Mode" if st.session_state.theme == "dark" else "🌙 Dark Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

    st.markdown(f"""
    <div style="padding:12px 0;font-size:0.7rem;color:var(--text-muted);text-align:center;">
        Session: {st.session_state.session_id}
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="sm-hero">
        <div class="sm-hero-eyebrow">AI-Powered Personal Styling</div>
        <div class="sm-hero-title">Your Mirror<br>Knows <span>Fashion</span></div>
        <div class="sm-hero-sub">Upload your photo and get a complete personalized style guide — 
        outfits, hairstyles, colors, and more — powered by Gemini AI.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    for col, val, lbl in zip(
        [col1, col2, col3],
        ["10+", "Free", "AI"],
        ["Features", "Forever", "Powered"]
    ):
        with col:
            st.markdown(f"""
            <div class="sm-stat-box" style="text-align:center;">
                <div class="sm-stat-value">{val}</div>
                <div class="sm-stat-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    section_header("✦", "What StyleMirror Does")

    features = [
        ("👁️", "Face Shape Analysis", "AI detects your face shape with confidence scoring"),
        ("👗", "Outfit Recommendations", "Complete looks for every occasion and budget"),
        ("💇", "Hairstyle Suggestions", "Cuts and styles tailored to your face shape"),
        ("💄", "Makeup & Grooming", "Look your best for any event"),
        ("💍", "Accessory Pairing", "Watches, jewelry, bags curated for you"),
        ("🎨", "Color Palette", "Your personal color season and best shades"),
        ("⭐", "Fashion Score", "Current score + actionable improvement plan"),
        ("📋", "Style Report", "A complete personalized style summary"),
        ("🔥", "Trend Explorer", "What's trending this season"),
        ("💬", "AI Chatbot", "Ask anything about fashion, get instant advice"),
    ]

    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="sm-card">
                <div style="font-size:1.4rem;margin-bottom:8px;">{icon}</div>
                <div class="sm-card-title">{title}</div>
                <div style="font-size:0.82rem;color:var(--text-muted);line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("📋", "How It Works")

    step_item(1, "Upload Your Photo",
              "Choose a clear front-facing photo (JPG, PNG). The better the photo, the better the results.")
    step_item(2, "Set Your Preferences",
              "Pick your occasion, season, budget, and style preference.")
    step_item(3, "Get Your Style Profile",
              "Gemini AI analyzes your photo and generates a complete personalized style guide.")
    step_item(4, "Explore & Save",
              "Browse all recommendations, chat with the AI stylist, and save your favorite looks.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✦  Start Your Style Analysis", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD & ANALYZE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "upload":
    section_header("📸", "Upload & Analyze")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="sm-card">', unsafe_allow_html=True)
        st.markdown('<div class="sm-card-title">Your Photo</div>', unsafe_allow_html=True)
        st.markdown('<div class="sm-card-subtitle">Front-facing, good lighting</div>',
                    unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose photo", type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        if uploaded:
            image = Image.open(uploaded)
            image = preprocess_image(image)
            st.session_state.uploaded_image = image
            st.image(image, use_container_width=True, caption="Your photo")
        elif st.session_state.uploaded_image:
            st.image(st.session_state.uploaded_image, use_container_width=True,
                     caption="Previously uploaded")
        else:
            st.markdown("""
            <div class="sm-upload-hint">
                📷 Upload a clear, front-facing photo<br>
                <small>JPG · JPEG · PNG · Max 5MB</small>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="sm-card">', unsafe_allow_html=True)
        st.markdown('<div class="sm-card-title">Your Preferences</div>', unsafe_allow_html=True)
        st.markdown('<div class="sm-card-subtitle">Personalize your recommendations</div>',
                    unsafe_allow_html=True)

        gender   = st.selectbox("Gender", GENDERS, key="gender_sel")
        occasion = st.selectbox("Occasion", OCCASIONS, key="occasion_sel")
        season   = st.selectbox("Season", SEASONS, key="season_sel")
        budget   = st.selectbox("Budget", BUDGETS, key="budget_sel")

        if budget == "Custom":
            custom_budget = st.text_input("Enter your budget (₹)", placeholder="e.g. ₹7,500")
            budget = custom_budget if custom_budget else "₹5,000"

        style_pref = st.selectbox("Style Preference", STYLE_PREFERENCES, key="style_sel")
        colors     = st.multiselect("Preferred Colors (optional)", COLOR_OPTIONS, key="color_sel")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.uploaded_image is not None:
        if st.button("✦  Analyze & Generate My Style Profile", use_container_width=True):
            image = st.session_state.uploaded_image

            # Determine effective API key (sidebar input > config > empty)
            from config import GEMINI_API_KEY
            api_key = st.session_state.get("user_gemini_api_key", "")
            if not api_key:
                try:
                    api_key = st.secrets.get("GEMINI_API_KEY", GEMINI_API_KEY)
                except Exception:
                    api_key = GEMINI_API_KEY

            _placeholder_keys = {"", "PASTE_YOUR_KEY_HERE", "your_gemini_api_key_here"}
            is_valid_key = bool(api_key and api_key.strip() and api_key not in _placeholder_keys)

            if is_valid_key and not st.session_state.get("api_key_validated", False):
                with st.spinner("Validating Gemini API key..."):
                    from fashion_engine.gemini_engine import validate_api_key
                    is_valid, _ = validate_api_key(api_key)
                    if not is_valid:
                        is_valid_key = False
                    else:
                        st.session_state.api_key_validated = True


            with st.spinner("Analyzing your photo with Gemini AI..."):
                # Store preferences
                st.session_state.gender    = gender
                st.session_state.occasion  = occasion
                st.session_state.season    = season
                st.session_state.budget    = budget
                st.session_state.style_pref = style_pref
                st.session_state.colors    = colors

                # Run face analysis
                face_data = analyze_face(image, gender)
                st.session_state.face_data = face_data

                progress = st.progress(0, text="Analyzing face...")

                progress.progress(15, text="Generating outfit recommendations...")
                outfit = get_outfit_recommendation(
                    face_data, occasion, season, budget, style_pref, colors, gender, image)

                progress.progress(30, text="Crafting hairstyle suggestions...")
                hair = get_hairstyle_recommendation(face_data, occasion, gender, image)

                progress.progress(45, text="Building makeup & grooming guide...")
                makeup = get_makeup_recommendation(face_data, occasion, gender, image)

                progress.progress(60, text="Selecting accessories...")
                accessories = get_accessory_recommendation(
                    face_data, outfit, occasion, budget, gender, image)

                progress.progress(72, text="Creating your color palette...")
                colors_data = get_color_palette(face_data, season, occasion, gender, image)

                progress.progress(84, text="Calculating fashion score...")
                score = get_fashion_score(face_data, occasion, style_pref, gender, image)

                progress.progress(94, text="Writing your style report...")
                report = get_full_style_report(
                    face_data, outfit, hair, makeup, accessories,
                    colors_data, score, occasion, season, budget, style_pref, gender)

                progress.progress(100, text="Done!")

                st.session_state.all_results = {
                    "outfit": outfit, "hair": hair, "makeup": makeup,
                    "accessories": accessories, "colors": colors_data,
                    "score": score, "report": report
                }
                st.session_state.analysis_done = True

            st.success("✦ Analysis complete! Explore your results in the sidebar.")
            st.balloons()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: OUTFIT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "outfit":
    section_header("👗", "Outfit Recommendations")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first to get outfit recommendations.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"
            st.rerun()
    else:
        outfit = st.session_state.all_results.get("outfit", {})
        fd     = st.session_state.face_data

        # Context badges
        ctx_cols = st.columns(4)
        for col, lbl, val in zip(
            ctx_cols,
            ["Occasion", "Season", "Budget", "Style"],
            [st.session_state.get("occasion",""), st.session_state.get("season",""),
             st.session_state.get("budget",""), st.session_state.get("style_pref","")]
        ):
            with col:
                st.markdown(f"""
                <div class="sm-stat-box">
                    <div style="font-size:0.7rem;color:var(--text-muted);
                                text-transform:uppercase;letter-spacing:0.1em;">{lbl}</div>
                    <div style="font-weight:600;color:var(--text-primary);
                                font-size:0.88rem;margin-top:4px;">{val}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns([3, 2], gap="large")

        with col_a:
            section_header("👕", "The Complete Look")
            outfit_item("👕", "Topwear", outfit.get("topwear", "—"))
            outfit_item("👖", "Bottomwear", outfit.get("bottomwear", "—"))
            outfit_item("👟", "Footwear", outfit.get("footwear", "—"))
            outfit_item("🧥", "Outerwear", outfit.get("outerwear", "—"))

            if outfit.get("outfit_description"):
                st.markdown(f"""
                <div class="sm-card" style="margin-top:8px;">
                    <div class="sm-card-subtitle">Overall Look</div>
                    <div style="color:var(--text-secondary);line-height:1.8;font-size:0.9rem;">
                        {outfit['outfit_description']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if outfit.get("why_it_works"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Why It Works For You</div>
                    <div style="color:var(--text-secondary);line-height:1.8;font-size:0.88rem;">
                        {outfit['why_it_works']}
                    </div>
                </div>""", unsafe_allow_html=True)

        with col_b:
            section_header("💰", "Budget Breakdown")
            bd = outfit.get("budget_breakdown", {})
            if bd:
                for item, price in bd.items():
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;
                                padding:10px 0;border-bottom:1px solid var(--border);
                                font-size:0.88rem;">
                        <span style="color:var(--text-secondary);text-transform:capitalize;">
                            {item}</span>
                        <span style="color:var(--accent-gold);font-weight:600;">{price}</span>
                    </div>""", unsafe_allow_html=True)

            if outfit.get("fabric_tips"):
                st.markdown(f"""
                <div class="sm-card" style="margin-top:16px;">
                    <div class="sm-card-subtitle">Fabric Tips</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {outfit['fabric_tips']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if outfit.get("style_hack"):
                st.markdown(f"""
                <div class="sm-card" style="background:var(--gradient-2);">
                    <div style="font-size:0.7rem;color:var(--accent-purple-light);
                                letter-spacing:0.15em;margin-bottom:6px;">✦ PRO STYLE HACK</div>
                    <div style="color:var(--text-primary);font-size:0.88rem;
                                line-height:1.7;font-style:italic;">
                        "{outfit['style_hack']}"
                    </div>
                </div>""", unsafe_allow_html=True)

            if outfit.get("shopping_tips"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Shopping Tips</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {outfit['shopping_tips']}
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HAIRSTYLE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "hair":
    section_header("💇", "Hairstyle Recommendations")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"; st.rerun()
    else:
        hair = st.session_state.all_results.get("hair", {})
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown(f"""
            <div class="sm-card">
                <div class="sm-card-subtitle">Recommended Style</div>
                <div class="sm-face-shape-name" style="font-size:1.8rem;text-align:left;margin-bottom:8px;">
                    {hair.get('recommended_hairstyle','—')}
                </div>
                <div style="color:var(--text-secondary);line-height:1.8;font-size:0.9rem;">
                    {hair.get('description','—')}
                </div>
            </div>""", unsafe_allow_html=True)

            if hair.get("why_suits_face"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Why This Suits Your Face</div>
                    <div style="color:var(--text-secondary);line-height:1.8;font-size:0.88rem;">
                        {hair['why_suits_face']}
                    </div>
                </div>""", unsafe_allow_html=True)

            steps = hair.get("styling_steps", [])
            if steps:
                section_header("📋", "Styling Steps")
                for i, step in enumerate(steps, 1):
                    step_item(i, f"Step {i}", step)

        with col2:
            if hair.get("alternative_styles"):
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Alternative Styles</div>
                """, unsafe_allow_html=True)
                for s in hair["alternative_styles"]:
                    st.markdown(f"""
                    <div style="padding:8px 0;border-bottom:1px solid var(--border);
                                font-size:0.85rem;color:var(--text-secondary);">
                        ✦ {s}
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if hair.get("products_needed"):
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Products Needed</div>
                """, unsafe_allow_html=True)
                for p in hair["products_needed"]:
                    st.markdown(f"""
                    <div style="padding:6px 0;font-size:0.85rem;color:var(--text-secondary);">
                        🛒 {p}
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if hair.get("color_suggestion"):
                st.markdown(f"""
                <div class="sm-card" style="background:var(--gradient-2);">
                    <div class="sm-card-subtitle">Color Suggestion</div>
                    <div style="color:var(--text-primary);font-size:0.88rem;line-height:1.7;">
                        {hair['color_suggestion']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if hair.get("hair_care_tip"):
                st.markdown(f"""
                <div class="sm-card">
                    <div style="font-size:0.7rem;color:var(--accent-gold);
                                letter-spacing:0.15em;margin-bottom:6px;">💛 HAIR CARE TIP</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {hair['hair_care_tip']}
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: MAKEUP
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "makeup":
    section_header("💄", "Makeup & Grooming")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"; st.rerun()
    else:
        makeup = st.session_state.all_results.get("makeup", {})
        gender = st.session_state.get("gender", "")

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            if makeup.get("overall_look"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">The Complete Look</div>
                    <div style="color:var(--text-secondary);line-height:1.8;font-size:0.9rem;">
                        {makeup['overall_look']}
                    </div>
                </div>""", unsafe_allow_html=True)

            for emoji, key, label in [
                ("🖐️", "base",   "Base / Foundation"),
                ("👁️", "eyes",   "Eyes"),
                ("💋", "lips",   "Lips"),
                ("🌸", "cheeks", "Cheeks & Contour"),
            ]:
                if makeup.get(key):
                    outfit_item(emoji, label, makeup[key])

            if makeup.get("key_technique"):
                st.markdown(f"""
                <div class="sm-card" style="background:var(--gradient-2);">
                    <div style="font-size:0.7rem;color:var(--accent-purple-light);
                                letter-spacing:0.15em;margin-bottom:6px;">✦ KEY TECHNIQUE</div>
                    <div style="color:var(--text-primary);font-size:0.88rem;line-height:1.7;">
                        {makeup['key_technique']}
                    </div>
                </div>""", unsafe_allow_html=True)

        with col2:
            if makeup.get("products_list"):
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Products List</div>
                """, unsafe_allow_html=True)
                for p in makeup["products_list"]:
                    st.markdown(f"""
                    <div style="padding:6px 0;font-size:0.85rem;color:var(--text-secondary);
                                border-bottom:1px solid var(--border);">🛒 {p}</div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if makeup.get("budget_tip"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Budget-Friendly Tip</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {makeup['budget_tip']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if makeup.get("longevity_tip"):
                st.markdown(f"""
                <div class="sm-card">
                    <div style="font-size:0.7rem;color:var(--accent-gold);
                                letter-spacing:0.15em;margin-bottom:6px;">⏱️ LONGEVITY TIP</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {makeup['longevity_tip']}
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ACCESSORIES
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "accessories":
    section_header("💍", "Accessory Recommendations")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"; st.rerun()
    else:
        acc = st.session_state.all_results.get("accessories", {})

        col1, col2 = st.columns(2, gap="large")

        with col1:
            section_header("✨", "Your Accessories")
            for emoji, key, label in [
                ("⌚", "watch",    "Watch"),
                ("💎", "jewelry",  "Jewelry"),
                ("🕶️", "eyewear",  "Eyewear"),
                ("👜", "bag",      "Bag"),
                ("👔", "belt",     "Belt"),
                ("🎩", "headwear", "Headwear"),
            ]:
                if acc.get(key):
                    outfit_item(emoji, label, acc[key])

        with col2:
            if acc.get("statement_piece"):
                st.markdown(f"""
                <div class="sm-card" style="background:var(--gradient-2);">
                    <div style="font-size:0.7rem;color:var(--accent-gold);
                                letter-spacing:0.15em;margin-bottom:8px;">✦ STATEMENT PIECE</div>
                    <div style="color:var(--text-primary);font-weight:600;
                                font-size:1rem;margin-bottom:8px;">
                        {acc['statement_piece']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if acc.get("avoid"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">❌ What to Avoid</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {acc['avoid']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if acc.get("budget_split"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Budget Allocation</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {acc['budget_split']}
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COLOR PALETTE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "colors":
    section_header("🎨", "Your Color Palette")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"; st.rerun()
    else:
        colors_data = st.session_state.all_results.get("colors", {})

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            if colors_data.get("color_season"):
                st.markdown(f"""
                <div class="sm-face-result">
                    <div style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;
                                color:var(--text-muted);margin-bottom:8px;">YOUR COLOR SEASON</div>
                    <div class="sm-face-shape-name">{colors_data['color_season']}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            section_header("🎨", "Primary Colors")
            primaries = colors_data.get("primary_colors", [])
            if primaries:
                color_palette_display(primaries)
                for c in primaries:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;
                                padding:10px 0;border-bottom:1px solid var(--border);">
                        <div style="width:28px;height:28px;border-radius:8px;
                                    background-color:{c.get('hex','#888888')};flex-shrink:0;
                                    border:2px solid rgba(255,255,255,0.15);
                                    box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>
                        <div>
                            <span style="font-weight:600;color:var(--text-primary);
                                         font-size:0.88rem;">{c.get('name','')}</span>
                            <span style="color:var(--text-muted);font-size:0.8rem;">
                                 · {c.get('hex','')}</span>
                            <div style="font-size:0.78rem;color:var(--text-muted);
                                        margin-top:2px;">{c.get('reason','')}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

        with col2:
            section_header("✨", "Accent Colors")
            accents = colors_data.get("accent_colors", [])
            if accents:
                color_palette_display(accents)

            if colors_data.get("avoid_colors"):
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">❌ Colors to Avoid</div>
                """, unsafe_allow_html=True)
                for c in colors_data["avoid_colors"]:
                    st.markdown(f"""
                    <div style="padding:6px 0;font-size:0.85rem;color:var(--text-secondary);
                                border-bottom:1px solid var(--border);">✗ {c}</div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if colors_data.get("combination_tip"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Best Combinations</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {colors_data['combination_tip']}
                    </div>
                </div>""", unsafe_allow_html=True)

            if colors_data.get("pattern_advice"):
                st.markdown(f"""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Pattern Advice</div>
                    <div style="color:var(--text-secondary);font-size:0.85rem;line-height:1.7;">
                        {colors_data['pattern_advice']}
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FASHION SCORE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "score":
    section_header("⭐", "Fashion Score")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"; st.rerun()
    else:
        score = st.session_state.all_results.get("score", {})

        col1, col2 = st.columns([2, 3], gap="large")

        with col1:
            score_display(
                score.get("current_score", 7.0),
                score.get("potential_score", 9.0),
                score.get("style_archetype", "The Stylish")
            )

            if score.get("celebrity_style_match"):
                st.markdown(f"""
                <div class="sm-card" style="text-align:center;margin-top:8px;">
                    <div class="sm-card-subtitle">Style Inspiration</div>
                    <div style="font-weight:600;color:var(--text-primary);font-size:0.95rem;">
                        {score['celebrity_style_match']}
                    </div>
                </div>""", unsafe_allow_html=True)

            # Breakdown scores
            breakdown = score.get("breakdown", {})
            if breakdown:
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">Score Breakdown</div>
                """, unsafe_allow_html=True)
                for category, val in breakdown.items():
                    label = category.replace("_", " ").title()
                    pct   = int((float(val) / 10) * 100)
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div style="display:flex;justify-content:space-between;
                                    font-size:0.8rem;color:var(--text-muted);margin-bottom:4px;">
                            <span>{label}</span><span>{val}/10</span>
                        </div>
                        <div class="sm-confidence-bar">
                            <div class="sm-confidence-fill" style="width:{pct}%"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            if score.get("strengths"):
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">✅ Your Strengths</div>
                """, unsafe_allow_html=True)
                for s in score["strengths"]:
                    st.markdown(f"""
                    <div style="padding:8px 0;border-bottom:1px solid var(--border);
                                font-size:0.88rem;color:var(--text-secondary);">
                        ✓ {s}
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if score.get("improvements"):
                st.markdown("""
                <div class="sm-card">
                    <div class="sm-card-subtitle">📈 Areas to Improve</div>
                """, unsafe_allow_html=True)
                for imp in score["improvements"]:
                    st.markdown(f"""
                    <div style="padding:8px 0;border-bottom:1px solid var(--border);
                                font-size:0.88rem;color:var(--text-secondary);">
                        → {imp}
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if score.get("quick_wins"):
                st.markdown("""
                <div class="sm-card" style="background:var(--gradient-2);">
                    <div style="font-size:0.7rem;color:var(--accent-gold);
                                letter-spacing:0.15em;margin-bottom:12px;">
                        ⚡ 3 QUICK WINS
                    </div>
                """, unsafe_allow_html=True)
                for i, win in enumerate(score["quick_wins"][:3], 1):
                    st.markdown(f"""
                    <div style="padding:8px 0;border-bottom:1px solid var(--border-accent);
                                font-size:0.88rem;color:var(--text-primary);">
                        <span style="color:var(--accent-gold);font-weight:700;">{i}.</span> {win}
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: STYLE REPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "report":
    section_header("📋", "Your Personalized Style Report")

    if not st.session_state.analysis_done:
        st.info("📸 Upload and analyze your photo first.")
        if st.button("Go to Upload"):
            st.session_state.page = "upload"; st.rerun()
    else:
        report   = st.session_state.all_results.get("report", "")
        face_data = st.session_state.face_data
        score    = st.session_state.all_results.get("score", {})

        # Summary stats
        st.markdown('<div class="sm-stats-row">', unsafe_allow_html=True)
        stats_html = ""
        stats_html += stat_box(face_data.get("face_shape","—"), "Face Shape")
        stats_html += stat_box(face_data.get("skin_tone","—"), "Skin Tone")
        stats_html += stat_box(f"{score.get('current_score','—')}", "Fashion Score")
        stats_html += stat_box(score.get("style_archetype","—").split(" ")[0] if score.get("style_archetype") else "—", "Archetype")
        st.markdown(stats_html + '</div>', unsafe_allow_html=True)

        # Report content
        st.markdown(f"""
        <div class="sm-report">
            {report.replace(chr(10), '<br>')}
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Save look button
        if st.button("💾  Save This Look to Gallery"):
            all_r = st.session_state.all_results
            save_look(st.session_state.session_id, {
                "occasion":     st.session_state.get("occasion",""),
                "season":       st.session_state.get("season",""),
                "budget":       st.session_state.get("budget",""),
                "style_pref":   st.session_state.get("style_pref",""),
                "face_shape":   face_data.get("face_shape",""),
                "gender":       st.session_state.get("gender",""),
                "outfit_rec":   all_r.get("outfit",{}).get("outfit_description",""),
                "hair_rec":     all_r.get("hair",{}).get("recommended_hairstyle",""),
                "makeup_rec":   all_r.get("makeup",{}).get("overall_look",""),
                "accessory_rec":all_r.get("accessories",{}).get("statement_piece",""),
                "color_palette":all_r.get("colors",{}).get("primary_colors",[]),
                "fashion_score":str(score.get("current_score","")),
                "full_report":  report,
            })
            st.success("✅ Look saved to your gallery!")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: TREND EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "trends":
    section_header("🔥", "Fashion Trend Explorer")

    col_filters = st.columns(2)
    with col_filters[0]:
        trend_season = st.selectbox("Season", SEASONS, key="trend_season")
    with col_filters[1]:
        trend_gender = st.selectbox("Gender", GENDERS, key="trend_gender")

    if st.button("✦  Explore Trends", use_container_width=True):
        # Validate API key first
        from config import GEMINI_API_KEY
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", GEMINI_API_KEY)
        except Exception:
            api_key = GEMINI_API_KEY
        
        with st.spinner("Fetching latest trends..."):
            trends = get_fashion_trends(trend_season, trend_gender)
            st.session_state.trends_data = trends
            
        if not api_key or api_key == "your_gemini_api_key_here" or api_key.strip() == "":
            st.info("💡 Showing default trends (Demo Mode). Add a Gemini key in `.streamlit/secrets.toml` for live trends.")
        else:
            if not st.session_state.get("api_key_validated", False):
                from fashion_engine.gemini_engine import validate_api_key
                is_valid, err_msg = validate_api_key(api_key)
                if not is_valid:
                    st.info(f"💡 Showing default trends (Demo Mode). Gemini key inactive: {err_msg}")
                else:
                    st.session_state.api_key_validated = True

    trends = st.session_state.get("trends_data", {})
    if trends:
        t1, t2 = st.columns(2, gap="large")

        with t1:
            section_header("👗", "Trending Outfits")
            for item in trends.get("trending_outfits", []):
                trend_card(
                    item.get("name",""),
                    item.get("description",""),
                    item.get("how_to_wear","")
                )

            section_header("✂️", "Trending Hairstyles")
            for style in trends.get("trending_hairstyles", []):
                st.markdown(f"""
                <div style="padding:10px 0;border-bottom:1px solid var(--border);
                            font-size:0.88rem;color:var(--text-secondary);">
                    ✦ {style}
                </div>""", unsafe_allow_html=True)

        with t2:
            section_header("🎨", "Trending Colors")
            for c in trends.get("trending_colors", []):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;
                            padding:12px 0;border-bottom:1px solid var(--border);">
                    <div style="width:36px;height:36px;border-radius:10px;
                                background-color:{c.get('hex','#888888')};flex-shrink:0;
                                border:2px solid rgba(255,255,255,0.15);
                                box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>
                    <div>
                        <div style="font-weight:600;color:var(--text-primary);
                                    font-size:0.88rem;">{c.get('name','')}</div>
                        <div style="font-size:0.72rem;color:var(--text-muted);">{c.get('hex','')}</div>
                        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:2px;">
                            {c.get('how_to_use','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

            section_header("🛍️", "Key Pieces This Season")
            for piece in trends.get("key_pieces", []):
                st.markdown(f"""
                <div style="padding:8px 0;border-bottom:1px solid var(--border);
                            font-size:0.85rem;color:var(--text-secondary);">
                    ✦ {piece}
                </div>""", unsafe_allow_html=True)

            if trends.get("seasonal_tip"):
                st.markdown(f"""
                <div class="sm-card" style="margin-top:16px;background:var(--gradient-2);">
                    <div style="font-size:0.7rem;color:var(--accent-purple-light);
                                letter-spacing:0.15em;margin-bottom:8px;">✦ STYLIST'S TIP</div>
                    <div style="color:var(--text-primary);font-size:0.88rem;line-height:1.7;">
                        {trends['seasonal_tip']}
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sm-upload-hint">
            🔥 Click "Explore Trends" to discover what's trending this season
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CHATBOT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "chatbot":
    section_header("💬", "AI Fashion Chatbot")

    # Check API key first
    from config import GEMINI_API_KEY
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", GEMINI_API_KEY)
    except Exception:
        api_key = GEMINI_API_KEY
    
    is_key_missing = not api_key or api_key == "your_gemini_api_key_here" or api_key.strip() == ""
    
    if is_key_missing:
        st.info("💡 Running Chatbot in Demo Mode (Mock Stylist active). Add a Gemini key in `.streamlit/secrets.toml` for live AI responses.")

    # Suggestions
    st.markdown("""
    <div style="margin-bottom:16px;">
        <div style="font-size:0.72rem;color:var(--text-muted);
                    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">
            Quick Questions
        </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "What should I wear for an interview?",
        "Which hairstyle suits my face?",
        "What colors look good on me?",
        "What to wear in summer under ₹2000?",
        "How to dress for a date night?",
        "What accessories should I buy?",
    ]

    cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_history.append(("user", sug))
                reply = fashion_chat(
                    sug,
                    st.session_state.chat_history[:-1],
                    st.session_state.face_data,
                    st.session_state.get("occasion", "")
                )
                if "API key not valid" in reply or "API_KEY_INVALID" in reply:
                    st.session_state.api_key_validated = False
                st.session_state.chat_history.append(("assistant", reply))
                save_chat_message(st.session_state.session_id, "user", sug)
                save_chat_message(st.session_state.session_id, "assistant", reply)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat window (only render the chat history box when there are active messages)
    if st.session_state.chat_history:
        st.markdown('<div class="sm-chat-container" id="chat-window">', unsafe_allow_html=True)
        for role, msg in st.session_state.chat_history:
            chat_message(role, msg)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Beautiful greeting banner instead of a giant empty box
        st.markdown("""
        <div style="text-align:center;padding:36px 20px;background:var(--gradient-2);border:1px solid var(--border);border-radius:16px;margin-bottom:20px;">
            <div style="font-size:2.2rem;margin-bottom:8px;background:var(--gradient-1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-family:'Playfair Display', serif;">✦ StyleMirror AI Stylist</div>
            <div style="font-size:0.92rem;color:var(--text-secondary);line-height:1.6;max-width:460px;margin:0 auto;">
                Hello! I am your personal AI fashion stylist. Click one of the quick questions above or type a message below to start curating your perfect look.
            </div>
        </div>""", unsafe_allow_html=True)

    # Input bar
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_msg = st.text_input(
            "Message", placeholder="Ask about fashion, styling, trends...",
            label_visibility="collapsed", key="chat_input"
        )
    with col_send:
        send = st.button("Send ✦", use_container_width=True)

    if send and user_msg.strip():
        st.session_state.chat_history.append(("user", user_msg))
        with st.spinner("Styling..."):
            reply = fashion_chat(
                user_msg,
                st.session_state.chat_history[:-1],
                st.session_state.face_data,
                st.session_state.get("occasion", "")
            )
        if "API key not valid" in reply or "API_KEY_INVALID" in reply:
            st.session_state.api_key_validated = False
        st.session_state.chat_history.append(("assistant", reply))
        save_chat_message(st.session_state.session_id, "user", user_msg)
        save_chat_message(st.session_state.session_id, "assistant", reply)
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SAVED LOOKS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "saved":
    section_header("🗂️", "Saved Looks Gallery")

    looks = get_saved_looks(st.session_state.session_id)

    if not looks:
        st.markdown("""
        <div class="sm-upload-hint" style="padding:48px;">
            <div style="font-size:2rem;margin-bottom:12px;">🗂️</div>
            <div>No saved looks yet. Analyze your photo and save your style report!</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:20px;">
            {len(looks)} saved look{'s' if len(looks) != 1 else ''}
        </div>""", unsafe_allow_html=True)

        for look in looks:
            (lid, occasion, season, budget, style_pref, face_shape,
             gender, outfit_rec, hair_rec, makeup_rec, accessory_rec,
             color_palette, fashion_score, full_report, created_at) = look

            with st.expander(f"✦  {occasion} · {season} · {created_at}", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    <div class="sm-stats-row">
                        {stat_box(face_shape, "Face Shape")}
                        {stat_box(fashion_score+"/10" if fashion_score else "—", "Score")}
                    </div>""", unsafe_allow_html=True)
                    if outfit_rec:
                        outfit_item("👗", "Outfit", outfit_rec)
                    if hair_rec:
                        outfit_item("💇", "Hairstyle", hair_rec)
                    if accessory_rec:
                        outfit_item("💍", "Statement Piece", accessory_rec)

                with c2:
                    if full_report:
                        st.markdown(f"""
                        <div class="sm-report" style="max-height:300px;overflow-y:auto;">
                            {full_report[:800].replace(chr(10),'<br>')}...
                        </div>""", unsafe_allow_html=True)

                if st.button(f"🗑️ Delete", key=f"del_{lid}"):
                    delete_look(lid)
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    section_header("ℹ️", "About StyleMirror AI")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="sm-card">
            <div class="sm-card-title">What is StyleMirror AI?</div>
            <div style="color:var(--text-secondary);line-height:1.9;font-size:0.88rem;margin-top:12px;">
                StyleMirror AI is a completely free, AI-powered personal fashion assistant that
                analyzes your photo and delivers a comprehensive style guide tailored specifically
                to your face shape, skin tone, preferences, occasion, and budget.
                <br><br>
                No model training, no datasets, no paid subscriptions — just upload your photo
                and get professional-grade styling advice instantly.
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="sm-card">
            <div class="sm-card-title">Technology Stack</div>
            <div style="margin-top:12px;">
        """, unsafe_allow_html=True)

        tech = [
            ("🧠", "Gemini 1.5 Flash", "All AI analysis, recommendations, and chatbot"),
            ("👁️", "OpenCV",           "Image preprocessing and face detection"),
            ("🖼️", "PIL / Pillow",      "Image enhancement and processing"),
            ("🎯", "Streamlit",         "Web interface and deployment"),
            ("🗄️", "SQLite",            "Saved looks and chat history"),
        ]
        for icon, name, desc in tech:
            st.markdown(f"""
            <div style="display:flex;gap:12px;padding:10px 0;
                        border-bottom:1px solid var(--border);align-items:flex-start;">
                <span style="font-size:1.2rem;">{icon}</span>
                <div>
                    <div style="font-weight:600;color:var(--text-primary);font-size:0.88rem;">
                        {name}</div>
                    <div style="font-size:0.78rem;color:var(--text-muted);">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="sm-card">
            <div class="sm-card-title">Features</div>
            <div style="margin-top:12px;">
        """, unsafe_allow_html=True)

        feats = [
            "AI Face Shape & Skin Tone Analysis",
            "Personalized Outfit Recommendations",
            "Hairstyle Suggestions",
            "Makeup & Grooming Guide",
            "Accessory Pairing",
            "Personal Color Palette",
            "Fashion Score (Current + Potential)",
            "Detailed Style Report",
            "Fashion Trend Explorer",
            "AI Fashion Chatbot",
            "Saved Looks Gallery",
            "Dark & Light Theme",
            "Occasion, Season & Budget Filters",
        ]
        for f in feats:
            st.markdown(f"""
            <div style="padding:6px 0;border-bottom:1px solid var(--border);
                        font-size:0.85rem;color:var(--text-secondary);">
                ✦ {f}
            </div>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="sm-card">
            <div class="sm-card-title">Deployment</div>
            <div style="color:var(--text-secondary);line-height:1.8;font-size:0.88rem;margin-top:12px;">
                Deploy for free on <strong style="color:var(--text-primary);">
                Streamlit Community Cloud</strong>.<br>
                Add your Gemini API key in Streamlit Secrets as
                <code style="background:var(--bg-hover);padding:2px 6px;
                             border-radius:4px;font-size:0.82rem;">GEMINI_API_KEY</code>.
            </div>
        </div>""", unsafe_allow_html=True)
