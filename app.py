import streamlit as st
import datetime
import io

# ReportLab Imports for PDF Generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Try importing pyswisseph safely for Streamlit Cloud deployment
try:
    import swisseph as swe
    HAS_SWISSEPH = True
except ImportError:
    HAS_SWISSEPH = False

# Set page configuration
st.set_page_config(
    page_title="MetaMatrix Destiny & Quantum Portal",
    page_icon="🧬",
    layout="wide"
)

# ==============================================================================
# 1. 22 ARCANA INTERPRETATION DICTIONARY
# ==============================================================================
ARCANA_DESCRIPTIONS = {
    1: {"title": "The Magician / The Pioneer", "energy": "Manifestation, Resourcefulness, Creation, New Beginnings"},
    2: {"title": "The High Priestess / Intuition", "energy": "Duality, Secret Knowledge, Subconscious, Inner Wisdom"},
    3: {"title": "The Empress / Abundance", "energy": "Fertility, Creation, Nurturing, Material Success"},
    4: {"title": "The Emperor / Authority", "energy": "Structure, Stability, Leadership, Mastery of Domain"},
    5: {"title": "The Hierophant / The Teacher", "energy": "Tradition, Spiritual Truth, Mentorship, Wisdom Transmission"},
    6: {"title": "The Lovers / Harmony", "energy": "Choice, Relationships, Alignment of Values, Partnership"},
    7: {"title": "The Chariot / Victory", "energy": "Willpower, Motion, Overcoming Obstacles, Focus"},
    8: {"title": "Justice / Equilibrium", "energy": "Karma, Balance, Truth, Cause and Effect"},
    9: {"title": "The Hermit / Wisdom", "energy": "Soul-Searching, Introspection, Inner Guidance, Expertise"},
    10: {"title": "Wheel of Fortune / Destiny Flow", "energy": "Cycles, Good Luck, Adaptation, Turning Points"},
    11: {"title": "Strength / Inner Power", "energy": "Courage, Compassion, Resilience, Passion Control"},
    12: {"title": "The Hanged Man / Perspective", "energy": "Pause, Surrender, New Enlightenment, Service"},
    13: {"title": "Death / Transformation", "energy": "Rebirth, Endings, Deep Evolution, Letting Go"},
    14: {"title": "Temperance / Alchemy", "energy": "Balance, Moderation, Flow, Higher Integration"},
    15: {"title": "The Devil / Shadow Alchemy", "energy": "Material Mastery, Unmasking Illusions, Freedom from Ties"},
    16: {"title": "The Tower / Breakthrough", "energy": "Sudden Awakening, Rebuilding, Breaking Chains"},
    17: {"title": "The Star / Higher Guidance", "energy": "Hope, Inspiration, Spiritual Purpose, Radiance"},
    18: {"title": "The Moon / Subconscious", "energy": "Intuition, Astral Realm, Overcoming Fear, Hidden Potential"},
    19: {"title": "The Sun / Radiant Success", "energy": "Joy, Leadership, Abundance, Vitality, Visibility"},
    20: {"title": "Judgement / Karma Clearance", "energy": "Family Healing, Awakening, Calling, Renewal"},
    21: {"title": "The World / Completion", "energy": "Wholeness, Global Connection, Fulfilment, Universal Success"},
    22: {"title": "The Fool / Infinite Potential", "energy": "Trust, Pure Potential, Freedom, Spiritual Journey"},
}

# ==============================================================================
# 2. MANIFESTATION / GRABOVOI CODES DATA
# ==============================================================================
MANIFESTATION_CODES = {
    "Money": {
        "Financial abundance": "318 798",
        "Unexpected money": "520 741 8",
        "Steady, long-term income": "9213140",
        "Cash flow abundance": "318 612 518 714",
        "Money knowledge": "964986583",
        "Money confidence": "87467894",
    },
    "Career": {
        "Manifest dream job": "493151 864 1491",
        "Get a job fast": "218 49451760",
        "Entrepreneurship": "71974131981",
    },
    "Love": {
        "Manifest love": "888 412 1289018",
        "Attract a partner": "197 023",
        "Self-love": "396815",
        "Eternal love": "888 912 818848",
        "Manifest romance": "401543512",
        "Reconnect with an ex": "89974476",
        "Reunite with a partner": "3856794",
    },
    "Well-Being": {
        "Good health": "80845700",
        "Healing of the body": "9187948181",
        "Weight management": "5343168",
        "Beauty and physical attraction": "83585179",
        "Spiritual Protection from Bullies": "55 16 987",
        "Addiction": "84 72 723",
        "Insomnia": "11 21 495",
        "Willpower": "35 31 798",
    },
    "Mind": {
        "Inner peace": "1001105010",
        "Cancel negativity": "4748132148",
        "Understanding": "39119488061",
        "Ideal future": "813791",
        "Positive Outlook": "25 67 993",
        "Gain Confidence": "45 32 246",
        "Focus": "45 88 623",
        "Fear": "42 58 735",
        "Anger": "66 82 121",
        "Betrayal": "53 14 80853",
    },
    "Health": {
        "Manifest Weight Loss": "5343168 31 22 778",
        "Hormonal Imbalance": "81 63 957",
        "Nourish Hair": "33 48 452",
        "Increased Muscle Flexibility & Strength": "81 21 596",
        "Wrinkles": "11112",
        "Cellulite": "2911",
    },
    "Other": {
        "Good luck": "817219738",
        "Fame": "8277237",
    },
}

# ==============================================================================
# 3. DESTINY MATRIX CALCULATION HELPERS
# ==============================================================================
def reduce_arcana(val: int) -> int:
    """Reduces numbers greater than 22 by summing their digits until <= 22."""
    while val > 22:
        val = sum(int(digit) for digit in str(val))
    return val

def calculate_destiny_matrix(dob: datetime.date):
    day = dob.day
    month = dob.month
    year = dob.year
    
    # Core Personal Square
    A = reduce_arcana(day)
    B = reduce_arcana(month)
    C = reduce_arcana(sum(int(d) for d in str(year)))
    D = reduce_arcana(A + B + C)
    E = reduce_arcana(A + B + C + D)  # Center/Comfort zone
    
    # Ancestral Cross
    F = reduce_arcana(A + B)  # Father Top-Left
    G = reduce_arcana(B + C)  # Mother Top-Right
    H = reduce_arcana(C + D)  # Ancestral Bottom-Right
    I = reduce_arcana(D + A)  # Ancestral Bottom-Left
    
    # Destinies
    sky = reduce_arcana(B + D)
    earth = reduce_arcana(A + C)
    personal_destiny = reduce_arcana(sky + earth)
    
    father_line = reduce_arcana(F + H)
    mother_line = reduce_arcana(G + I)
    social_destiny = reduce_arcana(father_line + mother_line)
    
    spiritual_destiny = reduce_arcana(personal_destiny + social_destiny)
    
    return {
        "A (Day/Personality)": A,
        "B (Month/Higher Self)": B,
        "C (Year/Karma)": C,
        "D (Bottom/Past Life)": D,
        "E (Center/Comfort Zone)": E,
        "F (Father Ancestral Top-Left)": F,
        "G (Mother Ancestral Top-Right)": G,
        "H (Ancestral Bottom-Right)": H,
        "I (Ancestral Bottom-Left)": I,
        "Sky Destiny": sky,
        "Earth Destiny": earth,
        "Personal Destiny": personal_destiny,
        "Social Destiny": social_destiny,
        "Spiritual Destiny": spiritual_destiny,
    }

# ==============================================================================
# 4. REPORTLAB PDF GENERATOR FUNCTION
# ==============================================================================
def generate_matrix_pdf(name, dob, matrix_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#4A154B"), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#1D1C1D"), spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6)
    
    # Header
    story.append(Paragraph(f"MetaMatrix Destiny Profile: {name}", title_style))
    story.append(Paragraph(f"<b>Date of Birth:</b> {dob.strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 12))
    
    # Matrix Table Data
    table_data = [["Node / Position", "Arcana Code", "Archetype Title", "Core Energy Essence"]]
    for key, val in matrix_data.items():
        arcana_info = ARCANA_DESCRIPTIONS.get(val, {"title": "Unknown", "energy": "Custom Energy"})
        table_data.append([
            key, 
            str(val), 
            arcana_info["title"], 
            arcana_info["energy"]
        ])
        
    t = Table(table_data, colWidths=[150, 60, 150, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4A154B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==============================================================================
# 5. STREAMLIT INTERFACE & ROUTING
# ==============================================================================
st.title("🧬 MetaMatrix Destiny & Quantum Portal")

tab1, tab2, tab3 = st.tabs(["🔮 Destiny Matrix Engine", "✨ Manifestation Codes", "🪐 Human Design / Ephemeris"])

# ------------------------------------------------------------------------------
# TAB 1: DESTINY MATRIX ENGINE
# ------------------------------------------------------------------------------
with tab1:
    st.header("Destiny Matrix Calculator")
    st.write("Enter birth details to calculate core energy nodes, ancestral lines, and download the full analysis PDF.")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        name_input = st.text_input("Full Name", value="Princess Jasmine")
    with col_input2:
        dob_input = st.date_input("Date of Birth", value=datetime.date(1985, 1, 1), min_value=datetime.date(1900, 1, 1))
        
    matrix_results = calculate_destiny_matrix(dob_input)
    
    st.markdown("---")
    st.subheader(f"✨ Destiny Matrix Profile for {name_input}")
    
    # Display Core Metrics
    col_res1, col_res2, col_res3 = st.columns(3)
    keys = list(matrix_results.keys())
    for idx, key in enumerate(keys):
        target_col = [col_res1, col_res2, col_res3][idx % 3]
        arc_val = matrix_results[key]
        arc_title = ARCANA_DESCRIPTIONS.get(arc_val, {}).get("title", "")
        with target_col:
            st.metric(label=key, value=f"Arcana {arc_val}", delta=arc_title)

    st.markdown("---")
    
    # Generate and Download PDF Report
    pdf_bytes = generate_matrix_pdf(name_input, dob_input, matrix_results)
    st.download_button(
        label="📄 Download Complete PDF Blueprint Report",
        data=pdf_bytes,
        file_name=f"{name_input.replace(' ', '_')}_Destiny_Matrix_Report.pdf",
        mime="application/pdf",
        type="primary"
    )

# ------------------------------------------------------------------------------
# TAB 2: MANIFESTATION CODES
# ------------------------------------------------------------------------------
with tab2:
    st.header("Grabovoi & Quantum Frequency Codes")
    
    categories = list(MANIFESTATION_CODES.keys())
    selected_category = st.selectbox("Select a Category:", categories)
    
    st.markdown("---")
    
    if selected_category:
        codes = MANIFESTATION_CODES[selected_category]
        col1, col2 = st.columns(2)
        
        for idx, (intention, code) in enumerate(codes.items()):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                st.subheader(f"✨ {intention}")
                st.code(code, language="text")

# ------------------------------------------------------------------------------
# TAB 3: HUMAN DESIGN / EPHEMERIS
# ------------------------------------------------------------------------------
with tab3:
    st.header("Human Design & Swiss Ephemeris Module")
    if HAS_SWISSEPH:
        st.success("Swiss Ephemeris (`pyswisseph`) module is compiled and ready for planetary calculations.")
    else:
        st.warning("`pyswisseph` build environment is active.")