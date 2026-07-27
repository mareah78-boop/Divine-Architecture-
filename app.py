import streamlit as st
import datetime
import ephem
import io
import math
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ==========================================
# 1. DICTIONARIES & LOOKUP DATA
# ==========================================

ARCANA_DICT = {
    1: ("The Magician", "Manifestation, resourcefulness, power, inspired action, creative energy."),
    2: ("The High Priestess", "Intuition, sacred knowledge, divine feminine, subconscious mind."),
    3: ("The Empress", "Femininity, beauty, nature, nurturing, abundance, creative fertility."),
    4: ("The Emperor", "Authority, structure, establishment, leadership, physical foundation."),
    5: ("The Hierophant", "Spiritual guidance, tradition, wisdom, mentorship, moral integrity."),
    6: ("The Lovers", "Relationships, harmony, choices, core values, deep soul alignment."),
    7: ("The Chariot", "Willpower, determination, victory, assertion, overcoming obstacles."),
    8: ("Justice", "Karma, cause and effect, truth, balance, accountability, divine law."),
    9: ("The Hermit", "Soul-searching, inner reflection, spiritual truth, solitude, wisdom."),
    10: ("Wheel of Fortune", "Cycles, luck, turning points, destiny, karma, adapting to life's flow."),
    11: ("Strength", "Inner power, courage, patience, compassion, mastery over human instincts."),
    12: ("The Hanged Man", "Surrender, new perspectives, letting go, pause, spiritual pause."),
    13: ("Death", "Transformation, endings, rebirth, transmuting old patterns, transition."),
    14: ("Temperance", "Balance, moderation, patience, alchemy, finding inner harmony."),
    15: ("The Devil / Shadow", "Shadow self, material attachments, temptation, overcoming limitations."),
    16: ("The Tower", "Sudden shift, awakening, dismantling illusions, breakthrough."),
    17: ("The Star", "Hope, faith, purpose, renewal, inspiration, spiritual illumination."),
    18: ("The Moon", "Illusion, fear, intuition, subconscious, navigating emotional depths."),
    19: ("The Sun", "Joy, success, celebration, vitality, clarity, divine warmth."),
    20: ("Judgement", "Rebirth, inner calling, absolution, awakening to purpose."),
    21: ("The World", "Completion, integration, accomplishment, global awareness, freedom."),
    22: ("The Fool", "New beginnings, innocence, spontaneous action, faith in the universe.")
}

GATE_DICTIONARY = {
    1: ("Self-Expression", "The power of unique creative identity and self-expression."),
    2: ("Higher Knowledge", "Receptivity, directional guidance, and receptive wisdom."),
    3: ("Ordering", "Overcoming chaos through structure and innovative solutions."),
    4: ("Formularization", "Mental solutions, logical answers, and seeking understanding."),
    5: ("Fixed Rhythms", "Natural timing, habits, consistency, and alignment with flow."),
    6: ("Friction", "Boundary creation, emotional clarity, and relational intimacy."),
    7: ("The Role of the Self", "Strategic leadership, guiding others, and logical direction."),
    8: ("Contribution", "Individual advocacy, standing out, and leading by example."),
    9: ("Focus", "Detail orientation, determination, and sustained concentration."),
    10: ("Behavior of the Self", "Self-love, authenticity, personal empowerment, and conviction."),
    11: ("Ideas", "Conceptual illumination, philosophy, and sharing visions."),
    12: ("Caution", "Artistic silence, social selectivity, and emotional restraint."),
    13: ("The Listener", "Empathy, gathering experiences, and holding secret wisdom."),
    14: ("Power Skills", "Resource accumulation, capacity for work, and generating prosperity."),
    15: ("Extremes", "Acceptance of diversity, rhythm variations, and human magnetic flow."),
    16: ("Selectivity", "Enthusiasm, skill acquisition, and technical mastery."),
    17: ("Opinions", "Logical concepts, future organization, and perspective."),
    18: ("Correction", "Improvement, identifying flaws, and perfecting patterns."),
    19: ("Wanting", "Sensitivity to basic needs, community support, and connection."),
    20: ("Metamorphosis", "Present moment awareness, immediate action, and presence."),
    21: ("Control", "Willpower, managing resources, authority, and self-reliance."),
    22: ("Openness", "Emotional grace, social influence, and deep listening."),
    23: ("Assimilation", "Translating complex ideas into simple, impactful insights."),
    24: ("Rationalization", "Mental processing, inner silence, and return to peace."),
    25: ("Spirit of the Self", "Universal love, innocence, vulnerability, and non-judgment."),
    26: ("Egoist", "Resourceful persuasion, efficient action, and boundary wisdom."),
    27: ("Caring", "Nurturing, accountability, boundaries, and supporting the collective."),
    28: ("The Game Player", "Perseverance through challenge, finding purpose, and courage."),
    29: ("Saying Yes", "Commitment to experience, devotion, and stamina."),
    30: ("Recognition of Feelings", "Desire processing, emotional passion, and acceptance of outcomes."),
    31: ("Democracy", "Inspirational leadership, voice of authority, and public influence."),
    32: ("Continuity", "Mindful reflection, processing experience, and enduring values."),
    33: ("Retreat", "Mindful reflection, processing experience, and gathering strength."),
    34: ("Power", "Pure instinctual energy, stamina, and self-governing force."),
    35: ("Change", "Hunger for experience, progression, and learning through cycle."),
    36: ("Crisis", "Emotional turmoil, navigating friction, and gaining maturity."),
    37: ("Friendship", "Family bonds, community agreement, and mutual support."),
    38: ("Fighter", "Standing up for integrity, finding meaning in struggle."),
    39: ("Provocation", "Dynamic catalyst, sparking spirit, and driving emotional growth."),
    40: ("Aloneness", "Ego rest, boundary setting, and balance between work and solitary retreat."),
    41: ("Contraction", "Inspiration, fuel for visualization, and human desire."),
    42: ("Growth", "Closing cycles, bringing projects to completion, and expansion."),
    43: ("Insight", "Inner breakthrough, unique perspective, and spontaneous clarity."),
    44: ("Alertness", "Instinctive awareness, learning from history, and pattern recognition."),
    45: ("Gathering Together", "Resource management, sovereignty, and communal stewardship."),
    46: ("Serendipity", "Love of the physical body, embodiment, and sensory appreciation."),
    47: ("Oppression", "Realization through reflection, transmuting mental hardship into wisdom."),
    48: ("Depth", "Intuitive solution, inner resourcefulness, and foundational wisdom."),
    49: ("Principles", "Rejection of unaligned norms, emotional boundary enforcement, revolution."),
    50: ("Values", "Guarding tribal integrity, responsibility, and establishing law."),
    51: ("Shock", "Initiation, competitive drive, and rousing spiritual awakening."),
    52: ("Stillness", "Meditation, grounding, holding focus under pressure."),
    53: ("Beginnings", "Initiating new phases, seed energy, and launching development."),
    54: ("Ambition", "Aspiration, drive for transformation, and spiritual material growth."),
    55: ("Abundance", "Spirit of freedom, emotional maturity, and intrinsic wealth."),
    56: ("Stimulation", "Storytelling, translating ideas, and experiential wisdom."),
    57: ("Intuitive Clarity", "Instinctive hearing, present-moment survival, and inner safety."),
    58: ("Vitality", "Joy of living, challenging unaligned authority, and perfecting life."),
    59: ("Sexuality", "Unifying intimacy, creative energy, and barrier removal."),
    60: ("Acceptance", "Transcending limitations, structure innovation, and steady evolution."),
    61: ("Mystery", "Inspiration for universal truths, inner knowing, and cosmic wonder."),
    62: ("Detail", "Precision, practical organization, and naming facts."),
    63: ("Doubt", "Logical inquiry, questioning truth, and critical verification."),
    64: ("Confusion", "Mental surrender, divine illumination, and creative processing.")
}

EXPANDED_GRABOVOI = {
    "Financial Abundance & Wealth Flow": {
        "Code": "71427321893",
        "Focus": "Attracting prosperity, unexpected monetary influx, financial security, and material stability."
    },
    "Harmonization of Relationships": {
        "Code": "5154868",
        "Focus": "Resolving interpersonal conflicts, fostering empathy, restoring balance, and deep soul connection."
    },
    "Self-Healing & Perfect Physical Health": {
        "Code": "1814321",
        "Focus": "Cellular regeneration, restoring organic balance, physical vitality, and immunity strengthening."
    },
    "Transforming Negative Energy to Light": {
        "Code": "19751",
        "Focus": "Clearing psychic blockages, transmuting dense external influences, and energetic protection."
    },
    "Spiritual Awakening & Intuitive Clarity": {
        "Code": "14888948",
        "Focus": "Opening the third eye, deepening meditation, receiving higher council, and spiritual expansion."
    },
    "Business Success & Project Mastery": {
        "Code": "21230990",
        "Focus": "Favorable outcome in ventures, attracting aligned clients, career acceleration, and execution."
    },
    "Unconditional Love & Heart Opening": {
        "Code": "8888888",
        "Focus": "Cultivating divine self-love, healing past heart trauma, and radiating light to surroundings."
    },
    "Time Acceleration / Goal Manifestation": {
        "Code": "918197185",
        "Focus": "Compressing timeline delays, accelerating intentions, and rapid alignment with desire."
    },
    "General Health & Immunity": {
        "Code": "1888948",
        "Focus": "Overall physical balance, energetic defense, and systemic body alignment."
    },
    "Harmonizing the Present Moment": {
        "Code": "71042",
        "Focus": "Anchoring presence, grounding anxiety, and aligning with immediate peace."
    },
    "Financial Independence": {
        "Code": "318 798",
        "Focus": "Releasing scarcity mindset, opening income streams, and energetic self-reliance."
    },
    "Determined Goal Achievement": {
        "Code": "894 719 7848",
        "Focus": "Laser focus, eliminating obstacles, and seeing long-term visions to completion."
    }
}

# ==========================================
# 2. CALCULATION ENGINES
# ==========================================

def reduce_arcana(val):
    val = abs(int(val))
    while val > 22:
        val = sum(int(digit) for digit in str(val))
    return 22 if val == 0 else val

def calculate_destiny_matrix(dob):
    day = dob.day
    month = dob.month
    year = dob.year
    A = reduce_arcana(day)
    B = reduce_arcana(month)
    C = reduce_arcana(year)
    D = reduce_arcana(A + B + C)
    E = reduce_arcana(A + B + C + D)
    F = reduce_arcana(A + B)
    G = reduce_arcana(B + C)
    H = reduce_arcana(C + D)
    I = reduce_arcana(D + A)
    era_20 = reduce_arcana(A + B)
    era_40 = reduce_arcana(B + C)
    era_60 = reduce_arcana(C + D)
    era_80 = reduce_arcana(D + A)
    chakras = {
        "Sahasrara (Crown)": {"Phys": A, "Energy": B, "Balance": reduce_arcana(A + B)},
        "Ajna (Third Eye)": {"Phys": reduce_arcana(A + E), "Energy": reduce_arcana(B + E), "Balance": reduce_arcana(reduce_arcana(A + E) + reduce_arcana(B + E))},
        "Vishuddha (Throat)": {"Phys": reduce_arcana(A + C), "Energy": reduce_arcana(B + D), "Balance": reduce_arcana(reduce_arcana(A + C) + reduce_arcana(B + D))},
        "Anahata (Heart)": {"Phys": E, "Energy": E, "Balance": reduce_arcana(E + E)},
        "Manipura (Solar Plexus)": {"Phys": reduce_arcana(C + E), "Energy": reduce_arcana(D + E), "Balance": reduce_arcana(reduce_arcana(C + E) + reduce_arcana(D + E))},
        "Svadhisthana (Sacral)": {"Phys": C, "Energy": D, "Balance": reduce_arcana(C + D)},
        "Muladhara (Root)": {"Phys": reduce_arcana(C + D), "Energy": reduce_arcana(D + A), "Balance": reduce_arcana(reduce_arcana(C + D) + reduce_arcana(D + A))}
    }
    return {
        "A": A, "B": B, "C": C, "D": D, "E": E,
        "F": F, "G": G, "H": H, "I": I,
        "era_20": era_20, "era_40": era_40, "era_60": era_60, "era_80": era_80,
        "chakras": chakras
    }

def longitude_to_gate(lon):
    deg = lon % 360
    gate_order = [
        41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60
    ]
    gate_index = int(deg / (360.0 / 64.0))
    gate = gate_order[gate_index % 64]
    rem = deg % (360.0 / 64.0)
    line = int(rem / ((360.0 / 64.0) / 6.0)) + 1
    return gate, line

def calculate_human_design_gates(dob, tob):
    dt_conscious = datetime.datetime.combine(dob, tob)
    dt_unconscious = dt_conscious - datetime.timedelta(days=88)
    ephem_date_conscious = ephem.Date(dt_conscious)
    ephem_date_unconscious = ephem.Date(dt_unconscious)
    bodies = {
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
    conscious_gates = {}
    unconscious_gates = {}
    for p_name, p_obj in bodies.items():
        p_obj.compute(ephem_date_conscious)
        ecl_long_c = float(ephem.Ecliptic(p_obj).lon) * (180.0 / math.pi)
        conscious_gates[p_name] = longitude_to_gate(ecl_long_c)
        p_obj.compute(ephem_date_unconscious)
        ecl_long_u = float(ephem.Ecliptic(p_obj).lon) * (180.0 / math.pi)
        unconscious_gates[p_name] = longitude_to_gate(ecl_long_u)
    return {"conscious": conscious_gates, "unconscious": unconscious_gates}

# ==========================================
# 3. PDF REPORT GENERATOR
# ==========================================

def generate_pdf_report(name, dob, tob, calc_data, hd_calc):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#2C3E50"), spaceAfter=10)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#16A085"), spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, leading=12, spaceAfter=4)
    table_cell_style = ParagraphStyle('TableCellStyle', parent=styles['Normal'], fontSize=8, leading=11)
    table_header_style = ParagraphStyle('TableHeaderStyle', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.whitesmoke, fontName="Helvetica-Bold")
    
    # Document Header
    story.append(Paragraph(f"<b>MetaMatrix Destiny Blueprint: {name}</b>", title_style))
    story.append(Paragraph(f"<b>Date of Birth:</b> {dob.strftime('%B %d, %Y')} | <b>Time of Birth:</b> {tob.strftime('%I:%M %p')}", body_style))
    story.append(Spacer(1, 8))
    
    # 1. Core Energy
    story.append(Paragraph("Core Energy & Personal Identity", heading_style))
    e_val = calc_data["E"]
    e_title, e_desc = ARCANA_DICT.get(e_val, ("Unknown", ""))
    story.append(Paragraph(f"<b>Center Soul Arcana (E): Arcana {e_val} — {e_title}</b>", body_style))
    story.append(Paragraph(e_desc, body_style))
    story.append(Spacer(1, 6))
    
    # Core Nodes Table
    story.append(Paragraph("Destiny Matrix Core Nodes", heading_style))
    node_data = [
        [
            Paragraph("<b>Node Position</b>", table_header_style),
            Paragraph("<b>Arcana</b>", table_header_style),
            Paragraph("<b>Archetype Title</b>", table_header_style),
            Paragraph("<b>Meaning</b>", table_header_style)
        ]
    ]
    raw_nodes = [
        ("Identity (A)", calc_data['A']),
        ("Spirituality (B)", calc_data['B']),
        ("Material Karma (C)", calc_data['C']),
        ("Physical Foundation (D)", calc_data['D']),
        ("Center Soul (E)", calc_data['E'])
    ]
    for label, val in raw_nodes:
        t_title, t_desc = ARCANA_DICT.get(val, ("",""))
        node_data.append([
            Paragraph(label, table_cell_style),
            Paragraph(str(val), table_cell_style),
            Paragraph(f"<b>{t_title}</b>", table_cell_style),
            Paragraph(t_desc, table_cell_style)
        ])
    t_nodes = Table(node_data, colWidths=[110, 45, 125, 260])
    t_nodes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_nodes)
    story.append(Spacer(1, 6))
    
    # Integration Guidance: Core Energy
    core_guide = "<b>Integration Guidance:</b> Use Center E as your primary soul baseline. Before taking action, audit whether you are acting out of high-frequency purpose or a low-frequency fear shadow."
    story.append(Paragraph(core_guide, table_cell_style))
    story.append(Spacer(1, 10))

    # 2. Ancestral Lines
    story.append(Paragraph("Ancestral & Lineage Support", heading_style))
    f_top_t, f_top_d = ARCANA_DICT.get(calc_data['F'], ('',''))
    f_bot_t, f_bot_d = ARCANA_DICT.get(calc_data['I'], ('',''))
    m_top_t, m_top_d = ARCANA_DICT.get(calc_data['G'], ('',''))
    m_bot_t, m_bot_d = ARCANA_DICT.get(calc_data['H'], ('',''))
    story.append(Paragraph(f"• <b>Father Line (Spirit Top - F):</b> Arcana {calc_data['F']} ({f_top_t}) — {f_top_d}", body_style))
    story.append(Paragraph(f"• <b>Father Line (Material Bottom - I):</b> Arcana {calc_data['I']} ({f_bot_t}) — {f_bot_d}", body_style))
    story.append(Paragraph(f"• <b>Mother Line (Spirit Top - G):</b> Arcana {calc_data['G']} ({m_top_t}) — {m_top_d}", body_style))
    story.append(Paragraph(f"• <b>Mother Line (Material Bottom - H):</b> Arcana {calc_data['H']} ({m_bot_t}) — {m_bot_d}", body_style))
    story.append(Spacer(1, 4))
    anc_guide = "<b>Integration Guidance:</b> Spirit nodes point to ancestral gifts ready to be reclaimed; Material nodes show inherited karmic themes to consciously resolve."
    story.append(Paragraph(anc_guide, table_cell_style))
    story.append(Spacer(1, 10))

    # 3. Destiny Eras
    story.append(Paragraph("Destiny Eras & 20-Year Cycles", heading_style))
    eras = [
        ("0 - 20 Years", calc_data['era_20']),
        ("20 - 40 Years", calc_data['era_40']),
        ("40 - 60 Years", calc_data['era_60']),
        ("60 - 80 Years", calc_data['era_80'])
    ]
    for era_label, era_val in eras:
        e_t, e_d = ARCANA_DICT.get(era_val, ('',''))
        story.append(Paragraph(f"• <b>{era_label}:</b> Arcana {era_val} ({e_t}) — {e_d}", body_style))
    story.append(Spacer(1, 10))

    # 4. Chakra Map
    story.append(Paragraph("7-Chakra Energy Alignment", heading_style))
    for c_name, vals in calc_data["chakras"].items():
        b_t, b_d = ARCANA_DICT.get(vals['Balance'], ('',''))
        story.append(Paragraph(f"• <b>{c_name}:</b> Harmonizer Arcana {vals['Balance']} ({b_t}) — {b_d}", body_style))
    story.append(Spacer(1, 10))

    # 5. Grabovoi Codes Section
    story.append(Paragraph("Grabovoi Manifestation Frequency Repository", heading_style))
    for code_name, code_info in EXPANDED_GRABOVOI.items():
        story.append(Paragraph(f"• <b>{code_name}:</b> Code <code>{code_info['Code']}</code> — {code_info['Focus']}", body_style))
    story.append(Spacer(1, 10))

    # 6. Human Design Section
    if hd_calc:
        story.append(Paragraph("Human Design Ephemeris Imprints", heading_style))
        story.append(Paragraph("<b>Conscious (Personality) Imprint:</b>", body_style))
        for p_name, (gate, line) in hd_calc["conscious"].items():
            gate_title, gate_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
            story.append(Paragraph(f"• <b>{p_name}:</b> Gate {gate}.{line} - <i>{gate_title}</i>: {gate_desc}", body_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Unconscious (Design) Imprint:</b>", body_style))
        for p_name, (gate, line) in hd_calc["unconscious"].items():
            gate_title, gate_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
            story.append(Paragraph(f"• <b>{p_name}:</b> Gate {gate}.{line} - <i>{gate_title}</i>: {gate_desc}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 4. STREAMLIT USER INTERFACE
# ==========================================

st.set_page_config(page_title="MetaMatrix Destiny Engine", page_icon="🔮", layout="wide")

st.title("🔮 MetaMatrix Destiny Engine")
st.markdown("---")

# User Input Controls
col1, col2, col3 = st.columns(3)
with col1:
    user_name = st.text_input("Full Name", value="First Middle Last")
with col2:
    dob = st.date_input("Date of Birth", value=datetime.date(1978, 12, 19))
with col3:
    time_unknown = st.checkbox("Time of Birth Unknown")
    if time_unknown:
        tob = datetime.time(12, 0)
        st.caption("Using 12:00 PM (Noon) default for calculation.")
    else:
        tob = st.time_input("Time of Birth", value=datetime.time(12, 0))

# Perform Calculations
calc_data = calculate_destiny_matrix(dob)
hd_calc = calculate_human_design_gates(dob, tob)

# Tab Navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "✨ Core & Nodes",
    "📜 Ancestral & Eras",
    "🧘 Chakra Alignment",
    "🪐 Human Design",
    "🔢 Grabovoi Codes",
    "📄 PDF Blueprint"
])

with tab1:
    st.header("Core Energy & Destiny Nodes")
    e_title, e_desc = ARCANA_DICT.get(calc_data['E'], ("",""))
    st.subheader(f"Center Soul Arcana (E): Arcana {calc_data['E']} — {e_title}")
    st.info(e_desc)
    st.subheader("Destiny Matrix Core Nodes Table")
    nodes_info = [
        ("Identity (A)", calc_data['A']),
        ("Spirituality (B)", calc_data['B']),
        ("Material Karma (C)", calc_data['C']),
        ("Physical Foundation (D)", calc_data['D']),
        ("Center Soul (E)", calc_data['E'])
    ]
    table_rows = []
    for pos, val in nodes_info:
        t, d = ARCANA_DICT.get(val, ("",""))
        table_rows.append({"Node Position": pos, "Arcana": val, "Archetype Title": t, "Meaning": d})
    st.table(table_rows)

    with st.expander("📖 How to Apply Your Core Energy Blueprint"):
        st.markdown("""
        * **Your Baseline Frequency:** Center E represents your primary soul frequency. Use this as your 'North Star' for big decisions.
        * **In Light vs. Shadow:** When making a decision, ask yourself if you are operating from your Arcana's core gift or its shadow fear response.
        * **Daily Action:** Notice where you feel friction today. Are you resisting your natural outward projection (Position A)?
        """)

with tab2:
    st.header("Ancestral Support & Destiny Eras")
    st.subheader("Ancestral Lines")
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        f_top_t, f_top_d = ARCANA_DICT.get(calc_data['F'], ('',''))
        st.write(f"**Father Line Spirit (F):** Arcana {calc_data['F']} - *{f_top_t}*")
        st.caption(f_top_d)
    with c_f2:
        f_bot_t, f_bot_d = ARCANA_DICT.get(calc_data['I'], ('',''))
        st.write(f"**Father Line Material (I):** Arcana {calc_data['I']} - *{f_bot_t}*")
        st.caption(f_bot_d)
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        m_top_t, m_top_d = ARCANA_DICT.get(calc_data['G'], ('',''))
        st.write(f"**Mother Line Spirit (G):** Arcana {calc_data['G']} - *{m_top_t}*")
        st.caption(m_top_d)
    with c_m2:
        m_bot_t, m_bot_d = ARCANA_DICT.get(calc_data['H'], ('',''))
        st.write(f"**Mother Line Material (H):** Arcana {calc_data['H']} - *{m_bot_t}*")
        st.caption(m_bot_d)
        
    with st.expander("📖 How to Apply Your Lineage Blueprint"):
        st.markdown("""
        * **Generational Gifts:** Lean into the Spirit nodes (F & G) to unlock innate ancestral gifts.
        * **Pattern Breaking:** Use Material nodes (I & H) to identify repetitive inherited cycles that are ready to be cleared.
        """)
        
    st.markdown("---")
    st.subheader("Destiny Eras (20-Year Life Cycles)")
    eras = [("0 - 20 Years", calc_data['era_20']), ("20 - 40 Years", calc_data['era_40']), ("40 - 60 Years", calc_data['era_60']), ("60 - 80 Years", calc_data['era_80'])]
    for era_label, val in eras:
        t, d = ARCANA_DICT.get(val, ('',''))
        st.write(f"• **{era_label}:** Arcana {val} ({t}) — {d}")

    with st.expander("📖 How to Apply Destiny Eras"):
        st.markdown("""
        * **Current Life Phase:** Identify your active 20-year cycle to align with its underlying growth lessons.
        * **Transition Seasons:** Focus on the theme of your upcoming era as you approach age milestones (20, 40, 60, 80).
        """)

with tab3:
    st.header("7-Chakra Energy Alignment Map")
    chakra_rows = []
    for c_name, vals in calc_data["chakras"].items():
        b_t, b_d = ARCANA_DICT.get(vals['Balance'], ('',''))
        chakra_rows.append({
            "Chakra": c_name,
            "Physical Node": vals['Phys'],
            "Energy Node": vals['Energy'],
            "Harmonizer Arcana": f"Arcana {vals['Balance']} - {b_t}",
            "Meaning": b_d
        })
    st.table(chakra_rows)

    with st.expander("📖 How to Apply Chakra Alignment"):
        st.markdown("""
        * **Somatic Auditing:** Scan physical or emotional blockages against the associated chakra level.
        * **Harmonizer Focus:** Meditate on the Harmonizer Arcana for any chakra feeling stagnant or overactive.
        """)

with tab4:
    st.header("Human Design Ephemeris Imprints")
    col_c, col_u = st.columns(2)
    with col_c:
        st.subheader("Conscious (Personality) Imprint")
        for p_name, (gate, line) in hd_calc["conscious"].items():
            g_title, g_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
            st.markdown(f"**{p_name}:** Gate {gate}.{line} - *{g_title}*")
            st.caption(g_desc)
    with col_u:
        st.subheader("Unconscious (Design) Imprint")
        for p_name, (gate, line) in hd_calc["unconscious"].items():
            g_title, g_desc = GATE_DICTIONARY.get(gate, ("Unknown Gate", ""))
            st.markdown(f"**{p_name}:** Gate {gate}.{line} - *{g_title}*")
            st.caption(g_desc)

    with st.expander("📖 How to Apply Human Design Imprints"):
        st.markdown("""
        * **Conscious (Black):** Your mind and personality traits—what you actively notice about yourself.
        * **Unconscious (Red):** Body wisdom and genetic patterns—what others often notice about you before you do.
        """)

with tab5:
    st.header("Grabovoi Manifestation Frequency Portal")
    st.markdown("Select an intention below to display its activation protocol.")
    selected_intent = st.selectbox("Choose Intention:", list(EXPANDED_GRABOVOI.keys()))
    code_data = EXPANDED_GRABOVOI[selected_intent]
    st.success(f"### Quantum Activation Code: **{code_data['Code']}**")
    st.write(f"**Focus & Purpose:** {code_data['Focus']}")
    st.subheader("Activation Protocol:")
    st.markdown("""
    1. **Visualize:** Focus on your sphere of consciousness in front of your heart space.
    2. **Vocalize:** Repeat each digit individually (e.g., *7 - 1 - 4 - 2...*).
    3. **Project:** Project light through the numbers into the physical cell structure or goal matrix.
    """)

with tab6:
    st.header("Generate Complete PDF Blueprint")
    st.markdown("Download a fully formatted PDF report including all Destiny Matrix nodes, ancestral support, chakras, Grabovoi codes, and Human Design imprints.")
    pdf_buffer = generate_pdf_report(user_name, dob, tob, calc_data, hd_calc)
    st.download_button(
        label="📥 Download Full PDF Blueprint",
        data=pdf_buffer,
        file_name=f"{user_name.replace(' ', '_')}_MetaMatrix_Blueprint.pdf",
        mime="application/pdf"
    )