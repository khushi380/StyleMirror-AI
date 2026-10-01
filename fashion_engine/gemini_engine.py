# pyrefly: ignore [missing-import]
import google.generativeai as genai
import streamlit as st
from PIL import Image
import io, base64, json, re, random
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_VISION_MODEL

# ─── Configure Gemini ──────────────────────────────────────────────────────────
def get_gemini_client():
    key = st.session_state.get("user_gemini_api_key", "")
    if not key:
        try:
            key = st.secrets.get("GEMINI_API_KEY", GEMINI_API_KEY)
        except Exception:
            key = GEMINI_API_KEY
    
    if not key or key in ("your_gemini_api_key_here", "PASTE_YOUR_KEY_HERE") or key.strip() == "":
        return None   # silently use mock fallback
    genai.configure(api_key=key)
    return genai

def validate_api_key(key: str) -> tuple[bool, str]:
    if not key or key == "your_gemini_api_key_here" or key.strip() == "":
        return False, "API key is empty or default placeholder."
    try:
        genai.configure(api_key=key)
        # Try a quick lightweight API call to verify the key
        for m in genai.list_models():
            break
        return True, ""
    except Exception as e:
        return False, str(e)

# ─── Image → Gemini ────────────────────────────────────────────────────────────
def pil_to_gemini(image: Image.Image):
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    return {"mime_type": "image/jpeg", "data": buf.read()}

# ─── Smart Mock Fallback Generator ─────────────────────────────────────────────
def get_mock_fallback(func_name: str, **kwargs) -> dict | str:
    gender = kwargs.get("gender", "Female")
    if "Prefer not to say" in gender or "Non-binary" in gender:
        gender = "Female"

    occasion = kwargs.get("occasion", "Casual Outing")
    season = kwargs.get("season", "Summer")
    budget = kwargs.get("budget", "₹3,000")
    style_pref = kwargs.get("style_pref", "Casual")
    colors = kwargs.get("colors", [])
    color_str = ", ".join(colors) if colors else "Blue"
    face_data = kwargs.get("face_data", {})
    face_shape = face_data.get("face_shape", "Oval")
    skin_tone = face_data.get("skin_tone", "Medium")
    undertone = face_data.get("undertone", "Neutral")
    
    if func_name == "analyze_face":
        shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong"]
        tones = ["Fair", "Light", "Medium", "Tan", "Deep"]
        undertones = ["Warm", "Cool", "Neutral"]
        hair_colors = ["Black", "Brown", "Blonde", "Red", "Grey"]
        hair_lengths = ["Short", "Medium", "Long"]
        
        return {
            "face_shape": random.choice(shapes),
            "confidence": random.randint(85, 95),
            "skin_tone": random.choice(tones),
            "undertone": random.choice(undertones),
            "hair_color": random.choice(hair_colors),
            "hair_length": random.choice(hair_lengths),
            "distinctive_features": "Defined cheekbones, balanced proportions, and expressive eyes.",
            "style_notes": "Your features are highly symmetrical. A balanced mix of soft outlines and structured edges will enhance your look."
        }

    elif func_name == "get_outfit_recommendation":
        if gender == "Male":
            if occasion in ["Office", "Interview", "Presentation"]:
                topwear = "Crisp white cotton Oxford shirt"
                bottomwear = "Charcoal grey slim-fit trousers"
                footwear = "Tan leather Oxford shoes"
                outerwear = "Navy blue structured blazer" if style_pref == "Formal" else "Not required"
            elif occasion in ["Wedding", "Festival"]:
                topwear = "Rich emerald green raw silk Kurta with gold embroidery"
                bottomwear = "Off-white cotton Churidar pajama"
                footwear = "Classic tan Juttis"
                outerwear = "Nehru jacket in cream silk"
            else:
                topwear = "Olive green breathable linen shirt"
                bottomwear = "Classic dark wash denim jeans"
                footwear = "Clean white minimalist sneakers"
                outerwear = "Black lightweight denim jacket" if season == "Winter" else "Not required"
        else:
            if occasion in ["Office", "Interview", "Presentation"]:
                topwear = "Pinstriped silk button-up blouse in beige"
                bottomwear = "Beige tailored trousers"
                footwear = "Classic pointed-toe nude heels"
                outerwear = "Black structured blazer"
            elif occasion in ["Wedding", "Festival"]:
                topwear = "Fuchsia pink georgette Anarkali kurta"
                bottomwear = "Matching flared palazzo pants"
                footwear = "Gold embellished block heels"
                outerwear = "Embroidered organza dupatta"
            else:
                topwear = "Lavender ribbed knit crop top" if season == "Summer" else "Mustard yellow oversized sweater"
                bottomwear = "High-waisted light wash straight-leg jeans"
                footwear = "White chunky platform sneakers"
                outerwear = "Oversized beige trench coat" if season == "Winter" else "Not required"

        # Parse numeric budget to dynamically allocate item costs without breaking the budget
        try:
            clean_b = budget.replace("₹", "").replace(",", "").replace("+", "").strip()
            budget_val = float(clean_b)
        except Exception:
            budget_val = 5000.0

        top_cost = int(budget_val * 0.35)
        bottom_cost = int(budget_val * 0.35)
        foot_cost = int(budget_val) - top_cost - bottom_cost

        return {
            "topwear": topwear,
            "bottomwear": bottomwear,
            "footwear": footwear,
            "outerwear": outerwear,
            "outfit_description": f"A highly curated and balanced {style_pref.lower()} look specifically selected for a {occasion.lower()} during {season.lower()}.",
            "why_it_works": f"The fit and silhouette complement your {face_shape} face shape. The selected colors highlight your {skin_tone.lower()} skin tone with a {undertone.lower()} undertone.",
            "fabric_tips": "Linen and organic cotton for comfort and breathability.",
            "budget_breakdown": {
                "topwear": f"₹{top_cost:,}",
                "bottomwear": f"₹{bottom_cost:,}",
                "footwear": f"₹{foot_cost:,}",
                "total": f"₹{int(budget_val):,}"
            },
            "shopping_tips": "Look for high-quality fabrics at retailers like Zara, H&M, or local boutique stores.",
            "style_hack": "Roll up your sleeves slightly and add a classic watch to immediately elevate the outfit structure."
        }

    elif func_name == "get_hairstyle_recommendation":
        if gender == "Male":
            recommended = "Classic Side Part with Low Fade" if occasion in ["Office", "Interview"] else "Textured Quiff with Matte Finish"
            description = "A clean-cut side part that highlights your cheekbones and jawline, offering a structured look."
            why_suits_face = f"Provides a nice height to balance out the symmetry of your {face_shape} face shape."
            steps = ["Blow-dry damp hair in the direction of the part", "Apply a dime-sized amount of pomade", "Comb or style with fingers"]
            products = ["Medium hold pomade", "Styling comb"]
            alts = ["Modern Pompadour", "Slicked Back Undercut"]
        else:
            recommended = "Sleek Low Bun" if occasion in ["Office", "Interview"] else "Soft Romantic Waves with Face-Framing Layers"
            description = "Gentle waves cascading down, framing the face beautifully and adding natural volume."
            why_suits_face = f"Softens the edges of a {face_shape} face, highlighting your eyes and smile."
            steps = ["Apply heat protectant to damp hair", "Blow dry using a round brush", "Use a curling wand on the lower halves"]
            products = ["Heat protectant spray", "Volumizing mousse"]
            alts = ["High Messy Ponytail", "Classic French Braid"]

        return {
            "recommended_hairstyle": recommended,
            "description": description,
            "why_suits_face": why_suits_face,
            "styling_steps": steps,
            "products_needed": products,
            "alternative_styles": alts,
            "hair_care_tip": "Apply a nourishing hair serum after washing to prevent frizz and enhance shine.",
            "color_suggestion": "Warm honey brown highlights to add dimension."
        }

    elif func_name == "get_makeup_recommendation":
        if gender == "Male":
            return {
                "base": "Hydrating moisturizer and mineral SPF 30+",
                "eyes": "Groomed eyebrows with clear brow gel",
                "lips": "Matte hydrating lip balm with shea butter",
                "cheeks": "Clean shave or well-groomed beard oil",
                "overall_look": "A clean, polished, fresh-faced grooming routine focused on healthy, hydrated skin.",
                "key_technique": "Exfoliate twice a week to avoid dry patches and razor bumps.",
                "products_list": ["Facial moisturizer", "Clear brow gel", "Nourishing lip balm"],
                "budget_tip": "Basic drugstore moisturizers with hyaluronic acid work wonderfully.",
                "longevity_tip": "Drink plenty of water and use a light moisturizer to keep skin looking fresh all day."
            }
        else:
            return {
                "base": "Dewy foundation or lightweight BB cream matching your tone",
                "eyes": "Subtle nude eyeshadow with thin winged eyeliner and mascara",
                "lips": "Dusty rose satin lipstick or tinted lip gloss",
                "cheeks": "Soft peach blush with a hint of highlighter on cheekbones",
                "overall_look": f"An elegant, fresh, and polished look suited perfectly for a {occasion.lower()}.",
                "key_technique": "Blend blush upwards towards the temples to lift your features.",
                "products_list": ["BB Cream", "Dusty Rose Lipstick", "Peach Blush", "Mascara"],
                "budget_tip": "High-quality drugstore brands offer exceptional pigments for shadow and blush.",
                "longevity_tip": "Spray a hydrating setting mist to lock the makeup in place for hours."
            }

    elif func_name == "get_accessory_recommendation":
        if gender == "Male":
            watch = "Minimalist silver analog watch with a black leather strap"
            jewelry = "Simple matte steel ring or subtle band"
            eyewear = "Classic black frame Wayfarer sunglasses"
            bag = "Leather messenger or laptop bag"
            belt = "Matching black leather belt"
            headwear = "Not required"
        else:
            watch = "Elegant rose gold watch with a slim mesh band"
            jewelry = "Minimalist gold hoop earrings and a delicate pendant necklace"
            eyewear = "Oversized cat-eye sunglasses"
            bag = "Sleek leather crossbody bag or clutch"
            belt = "Thin metallic waist belt"
            headwear = "Not required"

        return {
            "watch": watch,
            "jewelry": jewelry,
            "eyewear": eyewear,
            "bag": bag,
            "belt": belt,
            "headwear": headwear,
            "statement_piece": f"The elegant watch elevates your overall profile for {occasion}.",
            "avoid": f"Avoid heavy, oversized pieces that overwhelm your {face_shape} face shape.",
            "budget_split": "60% on watch & eyewear, 40% on jewelry/bags."
        }

    elif func_name == "get_color_palette":
        if occasion in ["Office", "Interview"]:
            primary = [
                {"name": "Navy Blue", "hex": "#1B3A6B", "reason": "Exudes trust and professionalism."},
                {"name": "Warm Beige", "hex": "#E1C699", "reason": "Sleek neutral base."},
                {"name": "Pure White", "hex": "#FFFFFF", "reason": "Crisp and classic."}
            ]
            accent = [
                {"name": "Deep Burgundy", "hex": "#800020", "reason": "Sophisticated touch of color."},
                {"name": "Steel Grey", "hex": "#708090", "reason": "Understated accent."}
            ]
        elif occasion in ["Wedding", "Festival"]:
            primary = [
                {"name": "Royal Blue", "hex": "#4169E1", "reason": "Rich and vibrant for celebratory settings."},
                {"name": "Maroon Red", "hex": "#800000", "reason": "Traditional yet highly elegant."},
                {"name": "Antique Gold", "hex": "#B59410", "reason": "Warm metallic festive tone."}
            ]
            accent = [
                {"name": "Emerald Green", "hex": "#50C878", "reason": "Beautiful contrast color."},
                {"name": "Fuchsia Pink", "hex": "#FF00FF", "reason": "Playful pop of color."}
            ]
        else:
            primary = [
                {"name": "Sage Green", "hex": "#87A96B", "reason": "Trendy, calm tone perfect for casual wear."},
                {"name": "Ivory Cream", "hex": "#FFFFF0", "reason": "Fresh, soft, and highly versatile."},
                {"name": "Slate Grey", "hex": "#708090", "reason": "Practical neutral anchor."}
            ]
            accent = [
                {"name": "Coral Pink", "hex": "#FF7F50", "reason": "Adds warmth and energy."},
                {"name": "Dusty Blue", "hex": "#4F86B0", "reason": "Cool understated tone."}
            ]

        return {
            "primary_colors": primary,
            "accent_colors": accent,
            "avoid_colors": ["Neon Yellow", "Mud Brown"],
            "color_season": "Spring/Summer" if season in ["Summer", "Monsoon"] else "Autumn/Winter",
            "combination_tip": f"Pair the first primary color with Ivory Cream for an effortlessly stylish {occasion.lower()} ensemble.",
            "pattern_advice": "Solid blocks or subtle stripes."
        }

    elif func_name == "get_fashion_score":
        curr = round(random.uniform(7.2, 7.9), 1)
        pot = round(curr + random.uniform(1.2, 1.8), 1)
        return {
            "current_score": curr,
            "potential_score": pot,
            "breakdown": {
                "fit_and_proportion": random.randint(7, 8),
                "color_coordination": random.randint(7, 8),
                "occasion_appropriateness": random.randint(8, 9),
                "accessory_game": random.randint(5, 7),
                "overall_style": random.randint(7, 8)
            },
            "strengths": [
                f"Excellent alignment with the {occasion} theme.",
                "Colors coordinate well with your skin undertones."
            ],
            "improvements": [
                "Accessory pairing could be more cohesive.",
                "Footwear selection can be refined to better match the outfit formality."
            ],
            "quick_wins": [
                "Incorporate a sleek leather belt matching your shoes.",
                "Add one statement accessory (e.g., minimalist watch or chain).",
                "Ensure proper fit at the shoulders and ankles."
            ],
            "style_archetype": "Modern Minimalist" if style_pref == "Minimalist" else "Contemporary Classic",
            "celebrity_style_match": "Timothée Chalamet" if gender == "Male" else "Zendaya"
        }

    return {}

# ─── 1. Face Analysis ──────────────────────────────────────────────────────────
def analyze_face(image: Image.Image, gender: str) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("analyze_face", gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    prompt = f"""
You are an expert fashion analyst and face shape specialist.
Analyze this person's face carefully. Gender: {gender}.

Return ONLY a valid JSON object with these exact keys:
{{
  "face_shape": "Oval|Round|Square|Heart|Diamond|Oblong",
  "confidence": 85,
  "skin_tone": "Fair|Light|Medium|Tan|Deep",
  "undertone": "Warm|Cool|Neutral",
  "hair_color": "Black|Brown|Blonde|Red|Grey|Other",
  "hair_length": "Short|Medium|Long",
  "distinctive_features": "brief description",
  "style_notes": "brief personalized note"
}}
Respond with ONLY the JSON. No explanation, no markdown.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in analyze_face: {e}. Falling back to smart mock.")
        return get_mock_fallback("analyze_face", gender=gender)

# ─── 2. Outfit Recommendation ──────────────────────────────────────────────────
def get_outfit_recommendation(face_data: dict, occasion: str, season: str,
                               budget: str, style_pref: str, colors: list,
                               gender: str, image: Image.Image) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("get_outfit_recommendation", face_data=face_data, occasion=occasion, season=season, budget=budget, style_pref=style_pref, colors=colors, gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    color_str = ", ".join(colors) if colors else "No preference"
    prompt = f"""
You are a world-class personal fashion stylist. Analyze the uploaded photo and provide a complete outfit recommendation.

Person Details:
- Gender: {gender}
- Face Shape: {face_data.get('face_shape', 'Oval')}
- Skin Tone: {face_data.get('skin_tone', 'Medium')} ({face_data.get('undertone', 'Neutral')} undertone)
- Occasion: {occasion}
- Season: {season}
- Budget: {budget}
- Style Preference: {style_pref}
- Preferred Colors: {color_str}

Return ONLY a valid JSON object with these exact keys:
{{
  "topwear": "specific item with color and fabric",
  "bottomwear": "specific item with color and fabric",
  "footwear": "specific recommendation",
  "outerwear": "jacket/layer if needed, else 'Not required'",
  "outfit_description": "2-3 sentence overall look description",
  "why_it_works": "explanation of why this suits their face shape and features",
  "fabric_tips": "fabric recommendations for the season",
  "budget_breakdown": {{
    "topwear": "estimated price",
    "bottomwear": "estimated price",
    "footwear": "estimated price",
    "total": "total estimate"
  }},
  "shopping_tips": "where and how to buy within budget",
  "style_hack": "one pro styling tip"
}}
Respond with ONLY the JSON. No markdown, no explanation.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_outfit_recommendation: {e}. Falling back to smart mock.")
        return get_mock_fallback("get_outfit_recommendation", face_data=face_data, occasion=occasion, season=season, budget=budget, style_pref=style_pref, colors=colors, gender=gender)

# ─── 3. Hairstyle Recommendation ───────────────────────────────────────────────
def get_hairstyle_recommendation(face_data: dict, occasion: str,
                                  gender: str, image: Image.Image) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("get_hairstyle_recommendation", face_data=face_data, occasion=occasion, gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    prompt = f"""
You are a celebrity hairstylist with 20 years of experience.

Person Details:
- Gender: {gender}
- Face Shape: {face_data.get('face_shape', 'Oval')}
- Current Hair: {face_data.get('hair_color', 'Black')}, {face_data.get('hair_length', 'Medium')} length
- Occasion: {occasion}

CRITICAL: The hairstyle MUST be specifically chosen for a '{occasion}' occasion.
Return ONLY a valid JSON object:
{{
  "recommended_hairstyle": "specific hairstyle name suited to {occasion}",
  "description": "how it looks, why it works for this occasion",
  "why_suits_face": "face shape compatibility explanation",
  "styling_steps": ["step 1", "step 2", "step 3"],
  "products_needed": ["product 1", "product 2"],
  "alternative_styles": ["style 1", "style 2"],
  "hair_care_tip": "one important hair care tip",
  "color_suggestion": "hair color recommendation if any"
}}
Respond with ONLY the JSON. No markdown, no explanation.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_hairstyle_recommendation: {e}. Falling back to smart mock.")
        return get_mock_fallback("get_hairstyle_recommendation", face_data=face_data, occasion=occasion, gender=gender)

# ─── 4. Makeup Recommendation ──────────────────────────────────────────────────
def get_makeup_recommendation(face_data: dict, occasion: str,
                               gender: str, image: Image.Image) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("get_makeup_recommendation", face_data=face_data, occasion=occasion, gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    prompt = f"""
You are a professional makeup artist and beauty consultant.

Person Details:
- Gender: {gender}
- Skin Tone: {face_data.get('skin_tone', 'Medium')}
- Undertone: {face_data.get('undertone', 'Neutral')}
- Face Shape: {face_data.get('face_shape', 'Oval')}
- Occasion: {occasion}

Return ONLY a valid JSON object:
{{
  "base": "foundation/BB cream recommendation with shade",
  "eyes": "eye makeup recommendation",
  "lips": "lip color and product",
  "cheeks": "blush/contour recommendation",
  "overall_look": "complete look description",
  "key_technique": "one technique to enhance their features",
  "products_list": ["product 1", "product 2", "product 3"],
  "budget_tip": "affordable alternatives",
  "longevity_tip": "how to make makeup last"
}}
If gender is Male, focus on grooming, skin care, and minimal enhancement.
Respond with ONLY the JSON. No markdown.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_makeup_recommendation: {e}. Falling back to smart mock.")
        return get_mock_fallback("get_makeup_recommendation", face_data=face_data, occasion=occasion, gender=gender)

# ─── 5. Accessory Recommendation ───────────────────────────────────────────────
def get_accessory_recommendation(face_data: dict, outfit_data: dict,
                                  occasion: str, budget: str,
                                  gender: str, image: Image.Image) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("get_accessory_recommendation", face_data=face_data, occasion=occasion, budget=budget, gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    prompt = f"""
You are a luxury accessories expert and personal stylist.

Person Details:
- Gender: {gender}
- Face Shape: {face_data.get('face_shape', 'Oval')}
- Skin Tone: {face_data.get('skin_tone', 'Medium')}
- Occasion: {occasion}
- Budget: {budget}
- Outfit: {outfit_data.get('outfit_description', 'Casual outfit')}

Return ONLY a valid JSON object:
{{
  "watch": "specific watch style recommendation",
  "jewelry": "necklace/bracelet/ring suggestions",
  "eyewear": "glasses/sunglasses frame style",
  "bag": "bag type and style",
  "belt": "belt recommendation if applicable",
  "headwear": "hat/cap if applicable, else 'Not needed'",
  "statement_piece": "one accessory to elevate the look",
  "avoid": "accessories to avoid for this face shape/occasion",
  "budget_split": "how to allocate accessory budget"
}}
Respond with ONLY the JSON. No markdown.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_accessory_recommendation: {e}. Falling back to smart mock.")
        return get_mock_fallback("get_accessory_recommendation", face_data=face_data, occasion=occasion, budget=budget, gender=gender)

# ─── 6. Color Palette ──────────────────────────────────────────────────────────
def get_color_palette(face_data: dict, season: str, occasion: str,
                       gender: str, image: Image.Image) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("get_color_palette", face_data=face_data, season=season, occasion=occasion, gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    prompt = f"""
You are a color theory expert and personal image consultant.

Person Details:
- Gender: {gender}
- Skin Tone: {face_data.get('skin_tone', 'Medium')}
- Undertone: {face_data.get('undertone', 'Neutral')}
- Season: {season}
- Occasion: {occasion}

Return ONLY a valid JSON object:
{{
  "primary_colors": [
    {{"name": "Color 1", "hex": "#HEX", "reason": "why it works"}},
    {{"name": "Color 2", "hex": "#HEX", "reason": "why it works"}},
    {{"name": "Color 3", "hex": "#HEX", "reason": "why it works"}}
  ],
  "accent_colors": [
    {{"name": "Accent 1", "hex": "#HEX", "reason": "why it works"}},
    {{"name": "Accent 2", "hex": "#HEX", "reason": "why it works"}}
  ],
  "avoid_colors": ["color 1", "color 2"],
  "color_season": "Spring|Summer|Autumn|Winter",
  "combination_tip": "best combination tip",
  "pattern_advice": "which patterns suit them"
}}
Respond with ONLY the JSON. No markdown.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_color_palette: {e}. Falling back to smart mock.")
        return get_mock_fallback("get_color_palette", face_data=face_data, season=season, occasion=occasion, gender=gender)

# ─── 7. Fashion Score ──────────────────────────────────────────────────────────
def get_fashion_score(face_data: dict, occasion: str, style_pref: str,
                       gender: str, image: Image.Image) -> dict:
    client = get_gemini_client()
    if not client:
        return get_mock_fallback("get_fashion_score", face_data=face_data, occasion=occasion, style_pref=style_pref, gender=gender)

    model  = genai.GenerativeModel(GEMINI_VISION_MODEL)
    prompt = f"""
You are a fashion critic and personal styling expert. Analyze the person's current look in the photo.

Context:
- Gender: {gender}
- Occasion: {occasion}
- Style Preference: {style_pref}
- Face Shape: {face_data.get('face_shape', 'Oval')}

Return ONLY a valid JSON object:
{{
  "current_score": 6.5,
  "potential_score": 9.0,
  "breakdown": {{
    "fit_and_proportion": 7,
    "color_coordination": 6,
    "occasion_appropriateness": 8,
    "accessory_game": 5,
    "overall_style": 6
  }},
  "strengths": ["what they are already doing well"],
  "improvements": ["specific actionable improvements"],
  "quick_wins": ["3 things to immediately improve"],
  "style_archetype": "The Minimalist | The Bold | The Classic",
  "celebrity_style_match": "celebrity name"
}}
Respond with ONLY the JSON. No markdown.
"""
    try:
        resp = model.generate_content([prompt, pil_to_gemini(image)])
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_fashion_score: {e}. Falling back to smart mock.")
        return get_mock_fallback("get_fashion_score", face_data=face_data, occasion=occasion, style_pref=style_pref, gender=gender)

# ─── 8. Full Style Report ──────────────────────────────────────────────────────
def get_full_style_report(face_data: dict, outfit_data: dict, hair_data: dict,
                           makeup_data: dict, accessory_data: dict,
                           color_data: dict, score_data: dict,
                           occasion: str, season: str, budget: str,
                           style_pref: str, gender: str) -> str:
    client = get_gemini_client()
    if not client:
        # Mock markdown report
        return f"""
## Your Style DNA
With a symmetrical **{face_data.get('face_shape', 'Oval')}** face shape, a **{face_data.get('skin_tone', 'Medium')}** skin tone, and **{face_data.get('undertone', 'Neutral')}** undertones, you have a highly versatile base. You can pull off a wide range of colors and cuts.

## The Perfect Look for {occasion}
For a {occasion.lower()} event in {season.lower()}, your ideal outfit features the **{outfit_data.get('topwear', 'Sage Green Shirt')}** paired with **{outfit_data.get('bottomwear', 'Ivory trousers')}**. This combination balances modern style with sophisticated proportions, keeping you elegant and comfortable.

## Hair & Beauty Highlights  
We recommend the **{hair_data.get('recommended_hairstyle', 'Textured Cut')}**. It perfectly complements your {face_data.get('face_shape', 'Oval')} shape by highlighting your natural structure. For grooming, keep things fresh with a **{makeup_data.get('base', 'Lightweight base')}** to maintain a natural look.

## Color Story
Your curated color palette is anchored in **{color_data.get('color_season', 'Spring')}** tones. Focus on colors like Navy Blue, Ivory, and Sage Green. Use Coral or Burgundy as accent tones for accessories to add a refined pop of color.

## Your Fashion Score & Growth Path
You currently score a **{score_data.get('current_score', '7.5')}/10** with the potential to reach **{score_data.get('potential_score', '9.2')}/10**. You can easily unlock your style potential by incorporating high-quality basics, aligning accessory colors, and ensuring precise tailoring.

## Final Stylist Note
Style is a form of self-expression. Wear what makes you feel confident, and don't be afraid to experiment with proportions and accessories to elevate your everyday looks!
"""

    model  = genai.GenerativeModel(GEMINI_MODEL)
    prompt = f"""
You are a senior fashion editor writing a personalized style report.

Based on this analysis data:
- Gender: {gender}
- Face Shape: {face_data.get('face_shape')} (Confidence: {face_data.get('confidence')}%)
- Skin Tone: {face_data.get('skin_tone')} with {face_data.get('undertone')} undertone
- Occasion: {occasion} | Season: {season} | Budget: {budget}
- Style: {style_pref}
- Outfit: {outfit_data.get('outfit_description', '')}
- Hairstyle: {hair_data.get('recommended_hairstyle', '')}
- Fashion Score: {score_data.get('current_score')}/10 → {score_data.get('potential_score')}/10
- Style Archetype: {score_data.get('style_archetype', '')}
- Color Season: {color_data.get('color_season', '')}

Write a warm, engaging, personalized style report (400-500 words) with these sections:
## Your Style DNA
## The Perfect Look for {occasion}
## Hair & Beauty Highlights  
## Color Story
## Your Fashion Score & Growth Path
## Final Stylist Note

Make it feel like advice from a personal stylist who genuinely cares. Be specific, warm, and actionable.
"""
    try:
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        print(f"Gemini API Exception in get_full_style_report: {e}. Falling back to smart mock.")
        # Fallback to standard mock report
        return f"""
## Your Style DNA
With a symmetrical **{face_data.get('face_shape', 'Oval')}** face shape, a **{face_data.get('skin_tone', 'Medium')}** skin tone, and **{face_data.get('undertone', 'Neutral')}** undertones, you have a highly versatile base. You can pull off a wide range of colors and cuts.

## The Perfect Look for {occasion}
For a {occasion.lower()} event in {season.lower()}, your ideal outfit features the **{outfit_data.get('topwear', 'Sage Green Shirt')}** paired with **{outfit_data.get('bottomwear', 'Ivory trousers')}**. This combination balances modern style with sophisticated proportions, keeping you elegant and comfortable.

## Hair & Beauty Highlights  
We recommend the **{hair_data.get('recommended_hairstyle', 'Textured Cut')}**. It perfectly complements your {face_data.get('face_shape', 'Oval')} shape by highlighting your natural structure. For grooming, keep things fresh with a **{makeup_data.get('base', 'Lightweight base')}** to maintain a natural look.

## Color Story
Your curated color palette is anchored in **{color_data.get('color_season', 'Spring')}** tones. Focus on colors like Navy Blue, Ivory, and Sage Green. Use Coral or Burgundy as accent tones for accessories to add a refined pop of color.

## Your Fashion Score & Growth Path
You currently score a **{score_data.get('current_score', '7.5')}/10** with the potential to reach **{score_data.get('potential_score', '9.2')}/10**. You can easily unlock your style potential by incorporating high-quality basics, aligning accessory colors, and ensuring precise tailoring.

## Final Stylist Note
Style is a form of self-expression. Wear what makes you feel confident, and don't be afraid to experiment with proportions and accessories to elevate your everyday looks!
"""

# ─── 9. Trends ────────────────────────────────────────────────────────────────
def get_fashion_trends(season: str, gender: str) -> dict:
    client = get_gemini_client()
    if not client:
        return {
            "trending_outfits": [
                {
                    "name": "Relaxed Linen Set",
                    "description": "Loose linen button-down shirt paired with matching wide-leg trousers.",
                    "how_to_wear": "Wear open over a white tank top with leather slide sandals."
                },
                {
                    "name": "Utility Workwear Jacket",
                    "description": "Heavy cotton canvas jacket with large pocket details in earth tones.",
                    "how_to_wear": "Pair with dark wash denim and chunky leather boots."
                }
            ],
            "trending_hairstyles": [
                "Modern Shag with Wispy Fringe",
                "Soft Mid-Fade with Textured Crops",
                "Sleek High Ponytail with Wrapped base"
            ],
            "trending_colors": [
                {"name": "Sage Green", "hex": "#87A96B", "how_to_use": "Excellent as a main layer or jacket color."},
                {"name": "Terracotta", "hex": "#E2725B", "how_to_use": "Incorporate via knitwear or suede accessories."}
            ],
            "key_pieces": [
                "Oversized Cotton Trenchcoat",
                "Chunky Minimalist Loafers",
                "Silver Chain Necklace"
            ],
            "seasonal_tip": "Focus on mixing textures: combine soft cottons with heavier utility outerwear to add depth to your outfits."
        }

    model  = genai.GenerativeModel(GEMINI_MODEL)
    prompt = f"""
You are a senior fashion director and trend analyst. Analyze and generate the key fashion trends for the season: '{season}' and gender: '{gender}'.

Return ONLY a valid JSON object with this exact structure:
{{
  "trending_outfits": [
    {{
      "name": "Outfit Style Name",
      "description": "Short description of the outfit/look",
      "how_to_wear": "Styling tip on how to wear it"
    }},
    {{
      "name": "Outfit Style Name 2",
      "description": "Short description",
      "how_to_wear": "Styling tip"
    }}
  ],
  "trending_hairstyles": [
    "Hairstyle 1",
    "Hairstyle 2",
    "Hairstyle 3"
  ],
  "trending_colors": [
    {{
      "name": "Color Name 1",
      "hex": "#HEXCODE",
      "how_to_use": "How to incorporate this color"
    }},
    {{
      "name": "Color Name 2",
      "hex": "#HEXCODE",
      "how_to_use": "How to incorporate this color"
    }}
  ],
  "key_pieces": [
    "Must-have item 1",
    "Must-have item 2",
    "Must-have item 3"
  ],
  "seasonal_tip": "Overall style/care advice for this season"
}}

Ensure all hex values are valid 6-character CSS hex codes (e.g., #2E4053).
Respond with ONLY the JSON. No markdown, no explanation.
"""
    try:
        resp = model.generate_content(prompt)
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Gemini API Exception in get_fashion_trends: {e}. Falling back to smart mock.")
        return {
            "trending_outfits": [
                {
                    "name": "Relaxed Linen Set",
                    "description": "Loose linen button-down shirt paired with matching wide-leg trousers.",
                    "how_to_wear": "Wear open over a white tank top with leather slide sandals."
                },
                {
                    "name": "Utility Workwear Jacket",
                    "description": "Heavy cotton canvas jacket with large pocket details in earth tones.",
                    "how_to_wear": "Pair with dark wash denim and chunky leather boots."
                }
            ],
            "trending_hairstyles": [
                "Modern Shag with Wispy Fringe",
                "Soft Mid-Fade with Textured Crops",
                "Sleek High Ponytail with Wrapped base"
            ],
            "trending_colors": [
                {"name": "Sage Green", "hex": "#87A96B", "how_to_use": "Excellent as a main layer or jacket color."},
                {"name": "Terracotta", "hex": "#E2725B", "how_to_use": "Incorporate via knitwear or suede accessories."}
            ],
            "key_pieces": [
                "Oversized Cotton Trenchcoat",
                "Chunky Minimalist Loafers",
                "Silver Chain Necklace"
            ],
            "seasonal_tip": "Focus on mixing textures: combine soft cottons with heavier utility outerwear to add depth to your outfits."
        }

# ─── 10. Chatbot ──────────────────────────────────────────────────────────────
def fashion_chat(user_message: str, chat_history: list,
                 face_data: dict = None, occasion: str = None,
                 image: Image.Image = None) -> str:
    client = get_gemini_client()
    if not client:
        # Simple rule-based mock responses for chat
        msg = user_message.lower()
        if "interview" in msg:
            return "For an interview, classic formalwear is always safe. A structured navy blue blazer, white cotton shirt, and charcoal trousers project competence and confidence. Keep accessories minimal: a simple watch and clean shoes."
        elif "color" in msg:
            return "Based on skin undertones, rich jewel tones (like Royal Blue and Emerald) look great on warm undertones, while cool undertones shine in crisp whites, silvers, and berry shades. Neutral undertones can wear almost anything!"
        elif "hairstyle" in msg:
            return "The best hairstyle depends on your face shape. Oval faces match almost anything. Round faces benefit from height (like a textured quiff or blowout), while square faces look great with softer layers or classic side parts."
        elif "summer" in msg or "budget" in msg or "price" in msg or "₹" in msg:
            return "Summer styling on a budget is easy! Focus on buying 3 versatile pieces: a neutral linen shirt, breathable cotton chinos, and comfortable sneakers. You can find high-quality options under ₹2000 at H&M, Westside, or Zara sales."
        else:
            return "That's a great fashion question! Generally, style is all about balance: if you wear a loose top, pair it with structured bottoms. Focus on color coordination, wear what makes you comfortable, and add one statement accessory to elevate the look."

    model = genai.GenerativeModel(GEMINI_MODEL)

    context = ""
    if face_data:
        context = f"""
User context from their photo analysis:
- Face Shape: {face_data.get('face_shape', 'Unknown')}
- Skin Tone: {face_data.get('skin_tone', 'Unknown')} ({face_data.get('undertone', 'Neutral')} undertone)
- Hair: {face_data.get('hair_color', 'Unknown')}, {face_data.get('hair_length', 'Unknown')} length
"""

    occasion_context = ""
    if occasion:
        occasion_context = f"""
The user's selected occasion is: {occasion}.
CRITICAL: If the user asks about style, outfit, colors, hairstyle, or accessories,
your advice MUST be specifically tailored for a '{occasion}' occasion.
Do NOT give generic advice — make it distinctly appropriate for '{occasion}'.
"""

    history_text = ""
    for msg in chat_history[-10:]:
        role = "User" if msg[0] == "user" else "Stylist"
        history_text += f"{role}: {msg[1]}\n"

    prompt = f"""
You are StyleMirror AI, a warm, knowledgeable personal fashion stylist and beauty consultant.
You give specific, actionable, personalized fashion advice.
You are encouraging, trendy, and practical.
{context}
{occasion_context}
Conversation so far:
{history_text}

User: {user_message}

Respond as the Stylist in a conversational, helpful tone. Keep response under 200 words.
Use specific recommendations when possible. Add relevant emojis sparingly.
"""
    try:
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        print(f"Gemini API Exception in fashion_chat: {e}. Falling back to rule-based mock.")
        # Fallback response
        msg = user_message.lower()
        if "interview" in msg:
            return "For an interview, classic formalwear is always safe. A structured navy blue blazer, white cotton shirt, and charcoal trousers project competence and confidence. Keep accessories minimal: a simple watch and clean shoes."
        elif "color" in msg:
            return "Based on skin undertones, rich jewel tones (like Royal Blue and Emerald) look great on warm undertones, while cool undertones shine in crisp whites, silvers, and berry shades. Neutral undertones can wear almost anything!"
        elif "hairstyle" in msg:
            return "The best hairstyle depends on your face shape. Oval faces match almost anything. Round faces benefit from height (like a textured quiff or blowout), while square faces look great with softer layers or classic side parts."
        elif "summer" in msg or "budget" in msg or "price" in msg or "₹" in msg:
            return "Summer styling on a budget is easy! Focus on buying 3 versatile pieces: a neutral linen shirt, breathable cotton chinos, and comfortable sneakers. You can find high-quality options under ₹2000 at H&M, Westside, or Zara sales."
        else:
            return "That's a great fashion question! Generally, style is all about balance: if you wear a loose top, pair it with structured bottoms. Focus on color coordination, wear what makes you comfortable, and add one statement accessory to elevate the look."
