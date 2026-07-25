import datetime
import math
import io
import streamlit as st
import swisseph as swe

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. ARCHETYPAL DICTIONARY & CORE DATA
# ==========================================

ARCHETYPES = {
    1: {"title": "The Magician", "theme": "Manifestation, Resourcefulness, Power", "shadow": "Manipulation, Unused Talent"},
    2: {"title": "The High Priestess", "theme": "Intuition, Sacred Knowledge, Inner Voice", "shadow": "Secrets, Disconnection from Self"},
    3: {"title": "The Empress", "theme": "Abundance, Nurturing, Creation", "shadow": "Stagnation, Over-dependence"},
    4: {"title": "The Emperor", "theme": "Structure, Authority, Stability", "shadow": "Rigidity, Control Issues"},
    5: {"title": "The Hierophant", "theme": "Wisdom, Spiritual Guidance, Tradition", "shadow": "Dogma, Blind Conformity"},
    6: {"title": "The Lovers", "theme": "Harmony, Choices, Deep Alignment", "shadow": "Indecision, Disharmony"},
    7: {"title": "The Chariot", "theme": "Willpower, Momentum, Victory", "shadow": "Aggression, Loss of Control"},
    8: {"title": "Justice / Strength", "theme": "Balance, Truth, Cause & Effect", "shadow": "Karma, Self-Deception"},
    9: {"title": "The Hermit", "theme": "Inner Light, Soul Introspection, Truth", "shadow": "Isolation, Loneliness"},
    10: {"title": "Wheel of Fortune", "theme": "Cycles, Destiny, Universal Flow", "shadow": "Bad Luck Mentality, Resistance"},
    11: {"title": "Strength / Passion", "theme": "Inner Fortitude, Grace, Energy Mastery", "shadow": "Self-Doubt, Repression"},
    12: {"title": "The Hanged One", "theme": "New Perspective, Surrender, Enlightenment", "shadow": "Victim Mindset, Stagnation"},
    13: {"title": "Death / Transformation", "theme": "Rebirth, Endings & Beginnings, Transition", "shadow": "Fear of Change, Clinging to Past"},
    14: {"title": "Temperance", "theme": "Alchemy, Balance, Patience", "shadow": "Extremes, Impatience"},
    15: {"title": "The Devil / Shadow", "theme": "Material Mastery, Unveiling Illusions, Passion", "shadow": "Addiction, Self-Limitation"},
    16: {"title": "The Tower", "theme": "Awakening, Breakthrough, Rebuilding", "shadow": "Sudden Destruction, Resistance to Truth"},
    17: {"title": "The Star", "theme": "Inspiration, Hope, Renewal", "shadow": "Discouragement, Loss of Faith"},
    18: {"title": "The Moon", "theme": "Subconscious, Dreams, Intuitive Gifts", "shadow": "Illusion, Unfounded Fear"},
    19: {"title": "The Sun", "theme": "Joy, Radiance, Success, Clarity", "shadow": "Ego, Burnout"},
    20: {"title": "Judgement / Rebirth", "theme": "Calling, Higher Purpose, Karma Resolution", "shadow": "Self-Doubt, Fear of Answering Call"},
    21: {"title": "The World", "theme": "Completion, Integration, Global Resonance", "shadow": "Incompletion, Limitation"},
    22: {"title": "The Fool / Zero Point", "theme": "Infinite Potential, Faith, New Beginnings", "shadow": "Recklessness, Naivety"}
}

# 64 Gate sequence in the Wheel starting from 0° Aries
GATE_SEQUENCE = [
    25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 20, 16, 35, 45, 12,
    15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6,
    46, 18, 48, 57, 32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11,
    10, 58, 38, 54, 61, 60, 41, 19, 13, 49, 30, 55, 37, 63, 22, 36
]

CHANNELS_MAP = {
    (1, 8): "Channel of Inspiration (Creative Role Model)",
    (2, 14): "Channel of the Beat (Keeper of Key & Direction)",
    (3, 60): "Channel of Mutation (Fluctuating Pulse of Change)",
    (4, 63): "Channel of Logic (Mental Ease & Doubt Resolution)",
    (5, 15): "Channel of Rhythm (Flowing with Life's Patterns)",
    (6, 59): "Channel of Mating (Emotional Openness & Bonding)",
    (7, 31): "Channel of the Alpha (Leadership for the Future)",
    (9, 52): "Channel of Concentration (Determined Focus)",
    (10, 20): "Channel of Awakening (Self-Love in Action)",
    (10, 34): "Channel of Exploration (Following One's Conscience)",
    (10, 57): "Channel of Perfected Form (Intuitive Survival Skill)",
    (11, 56): "Channel of Curiosity (The Seeker's Journey)",
    (12, 22): "Channel of Openness (Emotional Expression & Art)",
    (13, 33): "Channel of the Prodigal (The Witness & Historian)",
    (16, 48): "Channel of Wavelength (Mastery through Talent & Depth)",
    (17, 62): "Channel of Acceptance (Organizational Mind)",
    (18, 58): "Channel of Judgment (Desire to Perfect & Correct)",
    (19, 49): "Channel of Synthesis (Sensitivity & Community Needs)",
    (21, 45): "Channel of Money (Control & Material Resource)",
    (23, 43): "Channel of Structuring (Individual Insight Expressed)",
    (24, 61): "Channel of Awareness (Mental Inspiration & Mystery)",
    (25, 51): "Channel of Initiation (Leap into Unconditional Love)",
    (26, 44): "Channel of Surrender (Enterprise & Persuasion)",
    (27, 50): "Channel of Preservation (Nurturing & Values)",
    (28, 38): "Channel of Struggle (Finding Purpose in Life)",
    (29, 46): "Channel of Discovery (Succeeding where Others Fail)",
    (30, 41): "Channel of Recognition (Focused Desire & Dreams)",
    (32, 54): "Channel of Transformation (Ambition & Success)",
    (34, 20): "Channel of Charisma (Thoughts into Action)",
    (34, 57): "Channel of Power (Intuitive Instinctual Power)",
    (35, 36): "Channel of Transitoriness (Experiential Seeker)",
    (37, 40): "Channel of Community (Family & Emotional Bond)",
    (39, 55): "Channel of Emoting (Provoking Higher Moods)",
    (42, 53): "Channel of Maturation (Cyclical Growth & Cycles)",
    (47, 64): "Channel of Abstraction (Mental Clarity from Past)",
}

# ==========================================
# 2. HELPER CALCULATIONS & SWISS EPHEMERIS
# ==========================================

def reduce_energy(val: int) -> int:
    """Reduces values greater than 22 to fit the 22 Arcana system."""
    while val > 22:
        val = sum(int(digit) for digit in str(val))
    return val if val > 0 else 22

def calculate_core_matrix(day: int, month: int, year: int):
    """Calculates core matrix nodes using exact reduction rules."""
    crown = reduce_energy(day)
    karma = reduce_energy(month)
    
    year_sum = sum(int(d) for d in str(year))
    talent = reduce_energy(year_sum)
    
    base = reduce_energy(crown + karma + talent)
    soul = reduce_energy(crown + karma + talent + base)
    
    # Lineage Channels
    paternal_strength = reduce_energy(crown + talent)
    paternal_karma = reduce_energy(karma + base)
    maternal_strength = reduce_energy(crown + karma)
    maternal_karma = reduce_energy(talent + base)
    
    # Destiny Eras
    era_20_40 = reduce_energy(crown + karma)
    era_40_60 = reduce_energy(talent + base)
    spiritual_purpose = reduce_energy(soul + era_20_40 + era_40_60)
    
    return {
        "Crown": crown,
        "Karma": karma,
        "Talent": talent,
        "Base": base,
        "Soul": soul,
        "Paternal_Strength": paternal_strength,
        "Paternal_Karma": paternal_karma,
        "Maternal_Strength": maternal_strength,
        "Maternal_Karma": maternal_karma,
        "Era_20_40": era_20_40,
        "Era_40_60": era_40_60,
        "Spiritual_Purpose": spiritual_purpose
    }

def longitude_to_gate_and_line(lon: float):
    """Maps celestial longitude (0-360) directly to Human Design Gate & Line."""
    norm_lon = lon % 360.0
    gate_index = int(norm_lon / 5.625)
    gate = GATE_SEQUENCE[gate_index]
    
    remainder_deg = norm_lon % 5.625
    line = int(remainder_deg / 0.9375) + 1
    return gate, line

def calculate_human_design_gates(year, month, day, hour, minute, utc_offset_hours=0):
    """Calculates all 26 HD Gates using Swiss Ephemeris."""
    dt_local = datetime.datetime(year, month, day, hour, minute) - datetime.timedelta(hours=utc_offset_hours)
    
    julian_day_personality = swe.julday(
        dt_local.year, dt_local.month, dt_local.day, dt_local.hour + dt_local.minute / 60.0
    )
    
    bodies = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("North Node", swe.MEAN_NODE),
        ("Mercury", swe.MERCURY),
        ("Venus", swe.VENUS),
        ("Mars", swe.MARS),
        ("Jupiter", swe.JUPITER),
        ("Saturn", swe.SATURN),
        ("Uranus", swe.URANUS),
        ("Neptune", swe.NEPTUNE),
        ("Pluto", swe.PLUTO)
    ]
    
    personality_gates = {}
    
    # Personality (Conscious)
    for name, body in bodies:
        res = swe.calc_ut(julian_day_personality, body)
        lon = res[0][0]
        gate, line = longitude_to_gate_and_line(lon)
        personality_gates[name] = {"gate": gate, "line": line, "longitude": lon}
        
    sun_lon = personality_gates["Sun"]["longitude"]
    earth_lon = (sun_lon + 180.0) % 360.0
    e_gate, e_line = longitude_to_gate_and_line(earth_lon)
    personality_gates["Earth"] = {"gate": e_gate, "line": e_line, "longitude": earth_lon}
    
    nn_lon = personality_gates["North Node"]["longitude"]
    sn_lon = (nn_lon + 180.0) % 360.0
    sn_gate, sn_line = longitude_to_gate_and_line(sn_lon)
    personality_gates["South Node"] = {"gate": sn_gate, "line": sn_line, "longitude": sn_lon}
    
    # Design (Unconscious) ~88 degrees prior
    target_sun_lon = (sun_lon - 88.0) % 360.0
    jd_design = julian_day_personality - 88.0
    for _ in range(10):
        res = swe.calc_ut(jd_design, swe.SUN)
        curr_lon = res[0][0]
        diff = (curr_lon - target_sun_lon + 180) % 360 - 180
        if abs(diff) < 0.00001:
            break
        jd_design -= diff / 0.9856
        
    design_gates = {}
    for name, body in bodies:
        res = swe.calc_ut(jd_design, body)
        lon = res[0][0]
        gate, line = longitude_to_gate_and_line(lon)
        design_gates[name] = {"gate": gate, "line": line, "longitude": lon}
        
    d_sun_lon = design_gates["Sun"]["longitude"]
    d_earth_lon = (d_sun_lon + 180.0) % 360.0
    de_gate, de_line = longitude_to_gate_and_line(d_earth_lon)
    design_gates["Earth"] = {"gate": de_gate, "line": de_line, "longitude": d_earth_lon}
    
    d_nn_lon = design_gates["North Node"]["longitude"]
    d_sn_lon = (d_nn_lon + 180.0) % 360.0
    dsn_gate, dsn_line = longitude_to_gate_and_line(d_sn_lon)
    design_gates["South Node"] = {"gate": dsn_gate, "line": dsn_line, "longitude": d_sn_lon}
    
    # Calculate Active Channels
    all_active_gates = set(
        [v["gate"] for v in personality_gates.values()] + [v["gate"] for v in design_gates.values()]
    )
    
    defined_channels = []
    for (g1, g2), channel_name in CHANNELS_MAP.items():
        if g1 in all_active_gates and g2 in all_active_gates:
            defined_channels.append(f"Channel {g1}-{g2}: {channel_name}")
            
    return {
        "personality": personality_gates,
        "design": design_gates,
        "channels": defined_channels
    }

# ==========================================
# 3. PDF GENERATION ENGINE
# ==========================================

def generate_pdf_report(user_name, dob_str, matrix, hd_data=None):
    """Generates multi-page PDF report incorporating Matrix and Human Design data."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=15
    )
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=15,
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#333333')
    )
    
    story = []
    
    # Title & Header
    story.append(Paragraph("MetaMatrix Destiny & Human Design Analysis", title_style))
    story.append(Paragraph(f"<b>Client Profile:</b> {user_name} | <b>Birth Info:</b> {dob_str}", body_style))
    story.append(Spacer(1, 15))
    
    # Section 1: Core Matrix Nodes
    story.append(Paragraph("1. Core Matrix Archetypes", h2_style))
    table_data = [["Position", "Arcana #", "Archetype Title", "Core Manifestation Theme"]]
    
    core_positions = ["Crown", "Karma", "Talent", "Base", "Soul"]
    for pos in core_positions:
        val = matrix[pos]
        arch = ARCHETYPES[val]
        table_data.append([pos, str(val), arch['title'], arch['theme']])
        
    t = Table(table_data, colWidths=[80, 50, 150, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')])
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # Section 2: Lineage Channels & Purpose Eras
    story.append(Paragraph("2. Lineage Channels & Destiny Eras", h2_style))
    lineage_data = [
        ["Lineage / Era", "Arcana #", "Archetype", "Strategic Focus"],
        ["Paternal Strength", str(matrix['Paternal_Strength']), ARCHETYPES[matrix['Paternal_Strength']]['title'], ARCHETYPES[matrix['Paternal_Strength']]['theme']],
        ["Paternal Karma", str(matrix['Paternal_Karma']), ARCHETYPES[matrix['Paternal_Karma']]['title'], ARCHETYPES[matrix['Paternal_Karma']]['shadow']],
        ["Maternal Strength", str(matrix['Maternal_Strength']), ARCHETYPES[matrix['Maternal_Strength']]['title'], ARCHETYPES[matrix['Maternal_Strength']]['theme']],
        ["Maternal Karma", str(matrix['Maternal_Karma']), ARCHETYPES[matrix['Maternal_Karma']]['title'], ARCHETYPES[matrix['Maternal_Karma']]['shadow']],
        ["Era 20-40 Purpose", str(matrix['Era_20_40']), ARCHETYPES[matrix['Era_20_40']]['title'], ARCHETYPES[matrix['Era_20_40']]['theme']],
        ["Era 40-60 Purpose", str(matrix['Era_40_60']), ARCHETYPES[matrix['Era_40_60']]['title'], ARCHETYPES[matrix['Era_40_60']]['theme']],
        ["Spiritual Mission", str(matrix['Spiritual_Purpose']), ARCHETYPES[matrix['Spiritual_Purpose']]['title'], ARCHETYPES[matrix['Spiritual_Purpose']]['theme']]
    ]
    
    t2 = Table(lineage_data, colWidths=[120, 50, 140, 220])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')])
    ]))
    story.append(t2)
    
    # Section 3: Human Design Gates (if calculated)
    if hd_data:
        story.append(PageBreak())
        story.append(Paragraph("3. Human Design Planetary Gates", h2_style))
        
        # Channels
        if hd_data['channels']:
            story.append(Paragraph("<b>Defined Channels:</b>", body_style))
            for ch in hd_data['channels']:
                story.append(Paragraph(f"• {ch}", body_style))
            story.append(Spacer(1, 10))
            
        gate_rows = [["Planet", "Conscious Gate", "Unconscious Gate"]]
        planets = ["Sun", "Earth", "Moon", "North Node", "South Node", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        
        for p in planets:
            p_info = hd_data['personality'].get(p, {})
            d_info = hd_data['design'].get(p, {})
            
            p_str = f"Gate {p_info.get('gate','-')}.{p_info.get('line','-')}"
            d_str = f"Gate {d_info.get('gate','-')}.{d_info.get('line','-')}"
            gate_rows.append([p, p_str, d_str])
            
        t_hd = Table(gate_rows, colWidths=[120, 180, 180])
        t_hd.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#27AE60')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')])
        ]))
        story.append(t_hd)
        
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 4. STREAMLIT APPLICATION INTERFACE
# ==========================================

st.set_page_config(page_title="MetaMatrix Destiny & Human Design", layout="wide")

st.title("🌌 MetaMatrix Destiny & Human Design Analysis")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("📋 Client Input Profile")
user_name = st.sidebar.text_input("Full Name", value="Princess Jasmine")
birth_date = st.sidebar.date_input("Birth Date", datetime.date(1978, 12, 19))
birth_time = st.sidebar.time_input("Exact Birth Time", datetime.time(16, 58))
utc_offset = st.sidebar.number_input("UTC Offset (Hours)", min_value=-12.0, max_value=14.0, value=-5.0, step=0.5, help="e.g. -5 for EST, -6 for CST")

enable_hd = st.sidebar.checkbox("Calculate Human Design Gates", value=True)

# Calculate Matrix
matrix = calculate_core_matrix(birth_date.day, birth_date.month, birth_date.year)

# Calculate HD Gates if enabled
hd_data = None
if enable_hd:
    try:
        hd_data = calculate_human_design_gates(
            birth_date.year, birth_date.month, birth_date.day,
            birth_time.hour, birth_time.minute, utc_offset
        )
    except Exception as e:
        st.sidebar.error(f"HD Ephemeris Error: {e}")

# UI Tabs
tabs = st.tabs(["🏛️ Core Matrix Nodes", "🧬 Human Design Gates", "🌿 Lineage & Destiny", "📖 Archetype Dictionary", "📄 PDF Generator"])

# TAB 1: CORE MATRIX
with tabs[0]:
    st.subheader("Core Personal Matrix Alignments")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    positions = [("Crown", "Crown (Mind)"), ("Karma", "Karma (Emotional)"), ("Talent", "Talent (Skills)"), ("Base", "Base (Physical)"), ("Soul", "Soul Purpose")]
    cols = [c1, c2, c3, c4, c5]
    
    for (key, label), col in zip(positions, cols):
        val = matrix[key]
        arch = ARCHETYPES[val]
        with col:
            st.metric(label=label, value=f"{val} - {arch['title']}")
            st.caption(f"**Theme:** {arch['theme']}")
            st.caption(f"**Shadow:** {arch['shadow']}")

# TAB 2: HUMAN DESIGN GATES
with tabs[1]:
    st.subheader("Human Design Gate Imprints (Swiss Ephemeris)")
    
    if hd_data:
        if hd_data['channels']:
            st.success("### ⚡ Active Defined Channels")
            for ch in hd_data['channels']:
                st.markdown(f"* **{ch}**")
            st.markdown("---")
            
        col_p, col_d = st.columns(2)
        
        with col_p:
            st.markdown("### 🖤 Personality (Conscious Mind)")
            for planet, p_data in hd_data['personality'].items():
                st.write(f"**{planet}:** Gate **{p_data['gate']}**, Line **{p_data['line']}**")
                
        with col_d:
            st.markdown("### 🔴 Design (Unconscious Body)")
            for planet, d_data in hd_data['design'].items():
                st.write(f"**{planet}:** Gate **{d_data['gate']}**, Line **{d_data['line']}**")
    else:
        st.info("Enable Human Design Gates in the sidebar to view planetary gate coordinates.")

# TAB 3: LINEAGE & DESTINY
with tabs[2]:
    st.subheader("Ancestral Lineage & Destiny Eras")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🧬 Ancestral Lineage Channels")
        st.write(f"**Paternal Strength:** #{matrix['Paternal_Strength']} — {ARCHETYPES[matrix['Paternal_Strength']]['title']}")
        st.write(f"**Paternal Karma:** #{matrix['Paternal_Karma']} — {ARCHETYPES[matrix['Paternal_Karma']]['title']}")
        st.write(f"**Maternal Strength:** #{matrix['Maternal_Strength']} — {ARCHETYPES[matrix['Maternal_Strength']]['title']}")
        st.write(f"**Maternal Karma:** #{matrix['Maternal_Karma']} — {ARCHETYPES[matrix['Maternal_Karma']]['title']}")
        
    with col_b:
        st.markdown("### ⏳ Destiny Eras")
        st.write(f"**Era 20–40:** #{matrix['Era_20_40']} — {ARCHETYPES[matrix['Era_20_40']]['title']}")
        st.write(f"**Era 40–60:** #{matrix['Era_40_60']} — {ARCHETYPES[matrix['Era_40_60']]['title']}")
        st.write(f"**Spiritual Purpose:** #{matrix['Spiritual_Purpose']} — {ARCHETYPES[matrix['Spiritual_Purpose']]['title']}")

# TAB 4: ARCHETYPE DICTIONARY
with tabs[3]:
    st.subheader("The 22 Major Arcana Archetype Dictionary")
    for num, details in ARCHETYPES.items():
        with st.expander(f"Arcana {num}: {details['title']}"):
            st.write(f"**Theme:** {details['theme']}")
            st.write(f"**Shadow / Growth Area:** {details['shadow']}")

# TAB 5: PDF GENERATOR
with tabs[4]:
    st.subheader("Export Complete Profile PDF")
    st.write("Generate a formatted multi-page PDF document combining your MetaMatrix Nodes and Human Design Gate map.")
    
    dob_formatted = f"{birth_date.strftime('%B %d, %Y')} at {birth_time.strftime('%I:%M %p')}"
    
    if st.button("Generate Comprehensive PDF Report"):
        pdf_bytes = generate_pdf_report(user_name, dob_formatted, matrix, hd_data)
        st.download_button(
            label="💾 Download PDF Analysis Report",
            data=pdf_bytes,
            file_name=f"{user_name.replace(' ', '_')}_MetaMatrix_Analysis.pdf",
            mime="application/pdf"
        )