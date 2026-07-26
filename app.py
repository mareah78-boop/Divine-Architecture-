import streamlit as st
import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Try importing Ephem for astronomical calculations
try:
    import ephem
    HAS_EPHEM = True
except ImportError:
    HAS_EPHEM = False

# Set page layout
st.set_page_config(page_title="MetaMatrix Destiny", page_icon="🔮", layout="wide")

# ==========================================
# 1. LOOKUP DICTIONARIES
# ==========================================

ARCANA_DICT = {
    1: ("The Magician", "Manifestation, resourcefulness, power, active creation, initiative."),
    2: ("The High Priestess", "Intuition, sacred knowledge, subconscious, inner wisdom, mystery."),
    3: ("The Empress", "Fertility, abundance, nurturing, nature, creation, beauty."),
    4: ("The Emperor", "Structure, stability, authority, leadership, discipline, order."),
    5: ("The Hierophant", "Tradition, wisdom, spiritual teacher, order, values, mentorship."),
    6: ("The Lovers", "Choices, harmony, relationships, union, moral alignment."),
    7: ("The Chariot", "Determination, drive, victory, focus, overcoming obstacles."),
    8: ("Justice", "Karma, cause and effect, truth, balance, accountability."),
    9: ("The Hermit", "Inner reflection, soul-searching, solitude, spiritual truth."),
    10: ("Wheel of Fortune", "Cycles, luck, turning points, destiny, karma, flow."),
    11: ("Strength", "Inner power, courage, patience, compassion, mastery over instincts."),
    12: ("The Hanged Man", "Surrender, new perspective, pause, spiritual awakening."),
    13: ("Death", "Transformation, endings, rebirth, releasing the old, evolution."),
    14: ("Temperance", "Balance, moderation, alchemy, harmony, patience, integration."),
    15: ("The Devil", "Shadow self, temptation, attachments, material realm, liberation."),
    16: ("The Tower", "Breakthrough, upheaval, sudden illumination, structural shift."),
    17: ("The Star", "Hope, inspiration, spiritual guidance, renewal, clarity."),
    18: ("The Moon", "Illusion, dreams, subconscious fears, intuition, deep shadow."),
    19: ("The Sun", "Joy, success, vitality, expansion, leadership, radiance."),
    20: ("Judgment", "Rebirth, calling, ancestral karma, awakening, evaluation."),
    21: ("The World", "Completion, integration, global awareness, freedom, unity."),
    22: ("The Fool", "New beginnings, freedom, trust, leap of faith, innocence.")
}

GATE_DICTIONARY = {
    1: ("Self-Expression", "Creative power, individual purpose, and original leadership."),
    2: ("Higher Self", "Direction of the self, receptive wisdom, and inner alignment."),
    3: ("Ordering", "Overcoming chaos, establishing new structures, and innovation."),
    4: ("Formularization", "Mental solutions, logical answers, and seeking understanding."),
    5: ("Fixed Rhythms", "Natural timing, habits, consistency, and alignment with flow."),
    6: ("Friction", "Boundary management, intimacy, diplomacy, and emotional growth."),
    7: ("The Role of the Self", "Strategic leadership, guiding others, and logical direction."),
    8: ("Contribution", "Individual advocacy, standing out, and leading by example."),
    9: ("Focus", "Detail-oriented determination, concentration, and grounding."),
    10: ("Behavior of the Self", "Self-love, authenticity, personal empowerment, and conviction."),
    11: ("Ideas", "Conceptual wisdom, sharing visions, and inspiring potential."),
    12: ("Caution", "Artistic restraint, emotional articulation, and timing in expression."),
    13: ("The Listener", "Empathy, gathering experiences, and holding secret wisdom."),
    14: ("Power Skills", "Resource mastery, material energy, and sustained capacity."),
    15: ("Extremes", "Acceptance of diversity, magnetic rhythm, and adaptability."),
    16: ("Selectivity", "Enthusiasm, skill mastery, and deep identification with talent."),
    17: ("Opinions", "Logical foresight, organizing perspectives, and structured vision."),
    18: ("Correction", "Refining standards, instinct for improvement, and integrity."),
    19: ("Wanting", "Sensitivity to basic needs, community support, and connection."),
    20: ("The Present", "Existential awareness, immediate action, and clarity in the now."),
    21: ("Control", "Willpower, managing resources, authority, and self-reliance."),
    22: ("Openness", "Emotional grace, social influence, and depth of feeling."),
    23: ("Assimilation", "Translating complex ideas into simple, impactful insights."),
    24: ("Rationalization", "Mental processing, inner contemplation, and return to peace."),
    25: ("Spirituality", "Universal love, innocence, resilience, and unconditioned spirit."),
    26: ("The Egoist", "Persuasion, enterprise, efficient energy, and strategic action."),
    27: ("Caring", "Nurturing, accountability, boundaries, and supporting the collective."),
    28: ("The Game Player", "Perseverance, finding purpose through challenge, and bravery."),
    29: ("Commitment", "Saying yes to experience, devotion, and perseverance."),
    30: ("Recognition of Feelings", "Passionate desire, intensity, and emotional endurance."),
    31: ("Leading", "Democratic influence, voice of the public, and leadership by request."),
    32: ("Continuity", "Enduring values, instinct for viability, and adaptability."),
    33: ("Retreat", "Mindful reflection, processing experience, and gathering strength."),
    34: ("Power", "Pure sacral power, self-reliance, and constructive activity."),
    35: ("Change", "Hunger for experience, progression, and learning through cycle."),
    36: ("Crisis", "Emotional depth, overcoming turbulence, and transformative wisdom."),
    37: ("Friendship", "Family cohesion, tribal loyalty, and emotional agreement."),
    38: ("The Fighter", "Standing up for conviction, individual struggle, and resilience."),
    39: ("Provocation", "Dynamic catalyst, sparking spirit, and driving emotional growth."),
    40: ("Aloneness", "Willpower, boundaries between self and work, and quiet dedication."),
    41: ("Contraction", "Inspiration, fuel for visualization, and initiating new cycles."),
    42: ("Growth", "Closing loops, completing cycles, and bringing projects to fruition."),
    43: ("Insight", "Inner breakthrough, unique perspective, and spontaneous clarity."),
    44: ("Alertness", "Instinct for talent, historical memory, and pattern recognition."),
    45: ("The Gatherer", "Leadership of abundance, stewardship, and community wealth."),
    46: ("Determination", "Physical grounding, love of the body, and serendipity."),
    47: ("Realization", "Transmuting abstract pressure into sudden epiphany."),
    48: ("Depth", "Foundational wisdom, solution intuition, and resource capacity."),
    49: ("Principles", "Rejection of obsolete rules, transformation, and clear boundaries."),
    50: ("Values", "Guarding tribal integrity, responsibility, and establishing law."),
    51: ("Shock", "Initiation, willpower, awakening potential, and breaking boundaries."),
    52: ("Stillness", "Grounded concentration, quiet focus, and strategic pause."),
    53: ("Beginnings", "Initiating momentum, launching projects, and new foundations."),
    54: ("Ambition", "Drive for transformation, upward momentum, and spiritual aspiration."),
    55: ("Abundance", "Emotional freedom, spirit awareness, and inner wealth."),
    56: ("The Storyteller", "Sharing experience, stimulating inspiration, and wandering wisdom."),
    57: ("Intuitive Clarity", "Splenic instinct, acoustic sensitivity, and survival wisdom."),
    58: ("Joy of Life", "Vital energy, passion for betterment, and joyous drive."),
    59: ("Sexuality", "Breaking down barriers, intimacy, and generating connection."),
    60: ("Acceptance", "Working within structure, mutation through boundaries, and patience."),
    61: ("Mystery", "Universal truth, inspiration for the unknown, and inner knowing."),
    62: ("Details", "Precision in language, organizing facts, and clear naming."),
    63: ("Doubt", "Logical inquiry, questioning systems, and driving truth-seeking."),
    64: ("Confusion", "Processing mental imagery, abstract illumination, and clarity.")
}

GRABOVOI_CODES = {
    "Financial Abundance & Prosperity": "71427321893",
    "Harmonization of Relationships": "5154868",
    "Self-Healing & Perfect Health": "1814321",
    "Transforming Negative Energy": "19751",
    "Spiritual Awakening & Intuition": "14888948",
    "Success in Business & Projects": "21230990"
}

# Human Design 64 Gate wheel order (0° Aries start)
HD_GATE_ORDER = [
    25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 20, 16, 35, 45, 12,
    15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6,
    46, 18, 48, 57, 32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11,
    10, 58, 38, 54, 61, 60, 41, 19, 13, 49, 30, 55, 37, 63, 22, 36
]

# ==========================================
# 2. LOGIC & CALCULATION HELPERS
# ==========================================

def reduce_arcana(n: int) -> int:
    """Reduces numbers to 1-22 range using Destiny Matrix addition rule."""
    while n > 22:
        n = sum(int(digit) for digit in str(n))
    return n if n > 0 else 22

def calculate_destiny_matrix(dob: datetime.date):
    day = dob.day
    month = dob.month
    year = dob.year
    
    # Core Points
    A = reduce_arcana(day)
    B = reduce_arcana(month)
    C = reduce_arcana(sum(int(d) for d in str(year)))
    D = reduce_arcana(A + B + C)
    E = reduce_arcana(A + B + C + D)  # Center Soul Arcana
    
    # Ancestral Lines
    F = reduce_arcana(A + B)  # Father Line Top
    G = reduce_arcana(B + C)  # Mother Line Top
    H = reduce_arcana(C + D)  # Mother Line Bottom
    I_val = reduce_arcana(D + A)  # Father Line Bottom
    
    # Destiny Eras
    era_20 = reduce_arcana(A + E)
    era_40 = reduce_arcana(B + E)
    era_60 = reduce_arcana(C + E)
    era_80 = reduce_arcana(D + E)
    
    # Chakra Mapping
    chakras = {
        "Sahasrara (Crown)": {"Physical": A, "Energy": B, "Balance": reduce_arcana(A + B)},
        "Ajna (Third Eye)": {"Physical": reduce_arcana(A + E), "Energy": reduce_arcana(B + E), "Balance": reduce_arcana(reduce_arcana(A + E) + reduce_arcana(B + E))},
        "Vishuddha (Throat)": {"Physical": reduce_arcana(A + reduce_arcana(A + E)), "Energy": reduce_arcana(B + reduce_arcana(B + E)), "Balance": reduce_arcana(reduce_arcana(A + reduce_arcana(A + E)) + reduce_arcana(B + reduce_arcana(B + E)))},
        "Anahata (Heart)": {"Physical": E, "Energy": E, "Balance": reduce_arcana(E + E)},
        "Manipura (Solar Plexus)": {"Physical": reduce_arcana(D + E), "Energy": reduce_arcana(C + E), "Balance": reduce_arcana(reduce_arcana(D + E) + reduce_arcana(C + E))},
        "Svadhisthana (Sacral)": {"Physical": reduce_arcana(D + reduce_arcana(D + E)), "Energy": reduce_arcana(C + reduce_arcana(C + E)), "Balance": reduce_arcana(reduce_arcana(D + reduce_arcana(D + E)) + reduce_arcana(C + reduce_arcana(C + E)))},
        "Muladhara (Root)": {"Physical": D, "Energy": C, "Balance": reduce_arcana(D + C)}
    }
    
    return {
        "A": A, "B": B, "C": C, "D": D, "E": E,
        "F": F, "G": G, "H": H, "I": I_val,
        "era_20": era_20, "era_40": era_40, "era_60": era_60, "era_80": era_80,
        "chakras": chakras
    }

def longitude_to_gate(long_deg: float):
    """Converts ecliptic longitude degrees into Gate and Line."""
    long_deg = long_deg % 360.0
    gate_span = 360.0 / 64.0
    gate_idx = int(long_deg // gate_span)
    gate = HD_GATE_ORDER[gate_idx % 64]
    
    remainder = long_deg % gate_span
    line_span = gate_span / 6.0
    line = int(remainder // line_span) + 1
    return gate, line

def calculate_human_design_gates(dob: datetime.date, tob: datetime.time):
    if not HAS_EPHEM:
        return None
        
    dt_conscious = datetime.datetime.combine(dob, tob)
    ephem_date_conscious = ephem.Date(dt_conscious)
    ephem_date_unconscious = ephem.Date(dt_conscious - datetime.timedelta(days=88))
    
    planets = {
        "Sun": ephem.Sun(),
        "Moon": ephem.Moon(),
        "Mercury": ephem.Mercury(),
        "Venus": ephem.Venus(),
        "Mars": ephem.Mars(),
        "Jupiter": ephem.Jupiter(),
        "Saturn": ephem.Saturn(),
        "Uranus": ephem.Uranus(),
        "Neptune": ephem.Neptune(),
        "Pluto": ephem.Pluto()
    }
    
    conscious_gates, unconscious_gates = {}, {}
    
    for p_name, p_obj in planets.items():
        # Conscious
        p_obj.compute(ephem_date_conscious)
        ecl_long_c = float(ephem.Ecliptic(p_obj).lon) * (180.0 / 3.141592653589793)
        conscious_gates[p_name] = longitude_to_gate(ecl_long_c)
        
        # Unconscious
        p_obj.compute(ephem_date_unconscious)
        ecl_long_u = float(ephem.Ecliptic(p_obj).lon) * (180.0 / 3.141592653589793)
        unconscious_gates[p_name] = longitude_to_gate(ecl_long_u)
        
    return {"conscious": conscious_gates, "unconscious": unconscious_gates}

def generate_pdf_report(name, dob, tob, calc_data, hd_calc):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#2C3E50"), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#16A085"), spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6)
    
    # Title
    story.append(Paragraph(f"MetaMatrix Destiny Blueprint: {name}", title_style))
    story.append(Paragraph(f"<b>Date of Birth:</b> {dob.strftime('%B %d, %Y')} | <b>Time of Birth:</b> {tob.strftime('%I:%M %p')}", body_style))
    story.append(Spacer(1, 12))
    
    # Core Energy
    story.append(Paragraph("Core Energy & Personal Identity", heading_style))
    e_val = calc_data["E"]
    e_title, e_desc = ARCANA_DICT.get(e_val, ("Unknown", ""))
    story.append(Paragraph(f"<b>Center Soul Arcana (E): Arcana {e_val} — {e_title}</b>", body_style))
    story.append(Paragraph(e_desc, body_style))
    story.append(Spacer(1, 10))
    
    # Nodes Table
    story.append(Paragraph("Destiny Matrix Core Nodes", heading_style))
    node_data = [
        ["Node Position", "Arcana Number", "Archetype Title"],
        ["Personal Identity (A)", str(calc_data['A']), ARCANA_DICT.get(calc_data['A'], ("",""))[0]],
        ["Spiritual Connection (B)", str(calc_data['B']), ARCANA_DICT.get(calc_data['B'], ("",""))[0]],
        ["Material Karma (C)", str(calc_data['C']), ARCANA_DICT.get(calc_data['C'], ("",""))[0]],
        ["Physical Foundation (D)", str(calc_data['D']), ARCANA_DICT.get(calc_data['D'], ("",""))[0]],
        ["Center Soul Essence (E)", str(calc_data['E']), ARCANA_DICT.get(calc_data['E'], ("",""))[0]]
    ]
    t_nodes = Table(node_data, colWidths=[180, 100, 220])
    t_nodes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_nodes)
    story.append(Spacer(1, 12))
    
    # Human Design Section with Gate Descriptions
    if hd_calc:
        story.append(Paragraph("Human Design Ephemeris Imprints", heading_style))
        story.append(Spacer(1, 6))
        
        story.append(Paragraph("<b>Conscious (Personality) Imprint:</b>", body_style))
        for p_name, (gate, line) in hd_calc["conscious"].items():
            gate_title, gate_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
            text = f"• <b>{p_name}:</b> Gate {gate}.{line} - <i>{gate_title}</i>: {gate_desc}"
            story.append(Paragraph(text, body_style))
        
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Unconscious (Design) Imprint:</b>", body_style))
        for p_name, (gate, line) in hd_calc["unconscious"].items():
            gate_title, gate_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
            text = f"• <b>{p_name}:</b> Gate {gate}.{line} - <i>{gate_title}</i>: {gate_desc}"
            story.append(Paragraph(text, body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 3. STREAMLIT UI LAYOUT
# ==========================================

st.title("🔮 MetaMatrix Destiny")
st.markdown("##### *Integrated Destiny Matrix, Human Design Ephemeris & Manifestation System*")

# Sidebar
with st.sidebar:
    st.header("👤 Client Details")
    user_name = st.text_input("Full Name", "Princess Jasmine")
    dob = st.date_input("Date of Birth", datetime.date(1985, 8, 15), min_value=datetime.date(1920, 1, 1))
    tob = st.time_input("Time of Birth", datetime.time(12, 0))
    
    st.divider()
    st.session_state['user_name'] = user_name
    st.session_state['dob'] = dob
    st.session_state['tob'] = tob

calc = calculate_destiny_matrix(dob)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌟 Core Energy", 
    "🌳 Ancestral Lines", 
    "⏳ Destiny Eras", 
    "🧘 Chakra Map", 
    "✨ Manifestation Codes", 
    "🧬 Human Design"
])

with tab1:
    st.subheader("Core Energy & Personal Identity")
    e_val = calc["E"]
    e_title, e_desc = ARCANA_DICT.get(e_val, ("Unknown", ""))
    
    st.metric("Center Soul Arcana (E)", f"Arcana {e_val} — {e_title}")
    st.info(e_desc)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Node A (Identity)", calc['A'], ARCANA_DICT.get(calc['A'], ("",""))[0])
    col2.metric("Node B (Spirit)", calc['B'], ARCANA_DICT.get(calc['B'], ("",""))[0])
    col3.metric("Node C (Material)", calc['C'], ARCANA_DICT.get(calc['C'], ("",""))[0])
    col4.metric("Node D (Physical)", calc['D'], ARCANA_DICT.get(calc['D'], ("",""))[0])

with tab2:
    st.subheader("Ancestral & Lineage Support")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("### 👨‍👦 Father Line")
        st.write(f"**Top (F):** Arcana {calc['F']} — {ARCANA_DICT.get(calc['F'], ('',''))[0]}")
        st.write(f"**Bottom (I):** Arcana {calc['I']} — {ARCANA_DICT.get(calc['I'], ('',''))[0]}")
    with col_f2:
        st.markdown("### 👩‍👦 Mother Line")
        st.write(f"**Top (G):** Arcana {calc['G']} — {ARCANA_DICT.get(calc['G'], ('',''))[0]}")
        st.write(f"**Bottom (H):** Arcana {calc['H']} — {ARCANA_DICT.get(calc['H'], ('',''))[0]}")

with tab3:
    st.subheader("Destiny Eras & Life Progression")
    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    col_e1.metric("0 - 20 Years", f"Arcana {calc['era_20']}", ARCANA_DICT.get(calc['era_20'], ("",""))[0])
    col_e2.metric("20 - 40 Years", f"Arcana {calc['era_40']}", ARCANA_DICT.get(calc['era_40'], ("",""))[0])
    col_e3.metric("40 - 60 Years", f"Arcana {calc['era_60']}", ARCANA_DICT.get(calc['era_60'], ("",""))[0])
    col_e4.metric("60 - 80 Years", f"Arcana {calc['era_80']}", ARCANA_DICT.get(calc['era_80'], ("",""))[0])

with tab4:
    st.subheader("7-Chakra Energy Alignment")
    chakra_rows = []
    for c_name, vals in calc["chakras"].items():
        chakra_rows.append({
            "Chakra": c_name,
            "Physical Health": f"Arcana {vals['Physical']} ({ARCANA_DICT.get(vals['Physical'], ('',''))[0]})",
            "Energy & Emotions": f"Arcana {vals['Energy']} ({ARCANA_DICT.get(vals['Energy'], ('',''))[0]})",
            "Balance Point": f"Arcana {vals['Balance']} ({ARCANA_DICT.get(vals['Balance'], ('',''))[0]})"
        })
    st.table(chakra_rows)

with tab5:
    st.subheader("Grabovoi Manifestation Frequency Codes")
    for focus, code in GRABOVOI_CODES.items():
        st.write(f"**{focus}:** `{code}`")

with tab6:
    st.subheader("Human Design Ephemeris & Gate Imprints")
    if HAS_EPHEM:
        st.success("Ephemeris engine active!")
        hd_calc = calculate_human_design_gates(dob, tob)
        if hd_calc:
            col_hd1, col_hd2 = st.columns(2)
            
            with col_hd1:
                st.subheader("☀️ Conscious (Personality) Imprint")
                for p_name, (gate, line) in hd_calc["conscious"].items():
                    gate_title, gate_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
                    st.markdown(f"**{p_name}: Gate {gate}.{line} — {gate_title}**")
                    st.caption(gate_desc)

            with col_hd2:
                st.subheader("🧬 Unconscious (Design) Imprint")
                for p_name, (gate, line) in hd_calc["unconscious"].items():
                    gate_title, gate_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
                    st.markdown(f"**{p_name}: Gate {gate}.{line} — {gate_title}**")
                    st.caption(gate_desc)
    else:
        st.warning("Ephemeris engine initializing...")
        hd_calc = None

st.divider()

# PDF Download Section
hd_data_for_pdf = calculate_human_design_gates(dob, tob) if HAS_EPHEM else None
pdf_bytes = generate_pdf_report(user_name, dob, tob, calc, hd_data_for_pdf)

st.download_button(
    label="📄 Download Complete Detailed PDF Report",
    data=pdf_bytes,
    file_name=f"{user_name.replace(' ', '_')}_MetaMatrix_Blueprint.pdf",
    mime="application/pdf"
)